# previous part
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from .models import Actor, Movie, Genre, Rating
from .forms import ReviewForm, RatingForm


class GenreYear:
    """Жанры и года выхода фильмов"""
    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


# Старый вид/класс / записан через View()
# class MoviesView(View):
#     """Список фильмов"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movies.html", {"movie_list": movies})

class MoviesView(GenreYear, ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False) # вывести все кроме "черновиков"
    # template_name = "movies/movies.html"
    paginate_by = 2 # (пагинация) какое кол эл выводить на страницу


# class MovieDetailView(View):
#     """Полное описание фильма"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {"movie": movie})

class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    slug_field = 'url'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        context['form'] = ReviewForm()
        return context

# Вариант 1: с передачей id в форму
# class AddReview(View):
#     """Оставить отзыв"""
#     def post(self, request, pk):
#         form = ReviewForm(request.POST)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.movie_id = pk
#             form.save() # записываем (данные из формы) в БД
#         return redirect("/") #напр на Главную

# Вариант 2: с передачей целого обьекта Movie в форму
class AddReview(View):
    """Оставить отзыв"""
    def post(self, request, pk):
            form = ReviewForm(request.POST)
            movie = Movie.objects.get(id=pk)
            if form.is_valid():
                form = form.save(commit=False)
                if request.POST.get("parent", None):
                    form.parent_id = int(request.POST.get("parent"))
                form.movie = movie
                form.save() # записываем (данные из формы) в БД
            return redirect(movie.get_absolute_url()) #напр на эту же / обновляет страницу


class ActorView(GenreYear, DetailView):
    """Вывод информации о актёре"""
    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name"


class FilterMoviesView(ListView):
    """Фильтр фильмов"""
    paginate_by = 2

    def get_queryset(self):
        if 'genre' in self.request.GET and 'year' in self.request.GET:
            """Если выбраны и Жанр и Год"""
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")),
                Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct() # distinct() убирает повторяющиеся элементы
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) |
                Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join([
            f'year={x}&' for x in self.request.GET.getlist("year")
        ])
        context["genre"] = ''.join([
            f'genre={x}&' for x in self.request.GET.getlist("genre")
        ])
        return context


class JsonFilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов в json"""
    def get_queryset(self):
        if 'genre' in self.request.GET and 'year' in self.request.GET:
            """Если выбраны и Жанр и Год"""
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")),
                Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct().values("title", "tagline", "url", "poster")
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) |
                Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRaing(View):
    """Добавление рейтинга фильму"""
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск по фильмам"""
    paginate_by = 2

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get('q'))
    # __icontains чтоб не учитывался регистр

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['q'] = f'q={self.request.GET.get("q")}&'
        return context

#region === REST PART ==============================

from django.db import models # дописали [6]
from rest_framework import generics, permissions, viewsets # [14]
# from rest_framework.response import Response # удалили [9]
# from rest_framework.views import APIView # удалили [9]
from django_filters.rest_framework import DjangoFilterBackend

from .models import Movie, Actor
from .serializers import (
    MovieListSerializer,
    MovieDetailSerializer,
    ReviewCreateSerializer,
    CreateRatingSerializer,
    ActorListSelializer,
    ActorDetailSelializer
)
from .service import get_client_ip, MovieFilter, PaginationMovies

import time

'''
class MovieListView(generics.ListAPIView):
    """ [GET] Вывод списка фильмов [11]"""
    serializer_class = MovieListSerializer
    filter_backends = (DjangoFilterBackend,) #подключили фильт django
    filterset_class = MovieFilter # http://127.0.0.1:8001/api/v1/movie/?year_min=1983&year_max=2022&genres=Боевик
    permission_classes = [permissions.IsAuthenticated] # [12]

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies
'''

"""###########################################################################
*ReadOnlyModelViewSet - может выводить и список и одну запись
###########################################################################"""

class MovieViewSet(viewsets.ReadOnlyModelViewSet):
    """ [GET] Вывод списка фильмов [14] \n
    * ReadOnlyModelViewSet - может выводить и список и одну запись """
    filter_backends = (DjangoFilterBackend,) #подключили фильт django
    filterset_class = MovieFilter # http://127.0.0.1:8001/api/v1/movie/?year_min=1983&year_max=2022&genres=Боевик
    pagination_class = PaginationMovies
    # permission_classes = [permissions.IsAuthenticated] # Добавил

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Count("ratings", filter=models.Q(ratings__ip=get_client_ip(self.request)))
        ).annotate(
            middle_star=models.Sum(models.F('ratings__star')) / models.Count(models.F('ratings'))
        )
        return movies

    def get_serializer_class(self):
        if self.action == 'list':
            start = time.time()
            m = MovieListSerializer
            end = time.time()
            tracker = [end - start]
            print(f'{tracker=} {start=} {end=}')
            return m
            # return serialize_movie()
        elif self.action == 'retrieve':
            return MovieDetailSerializer
    #-----------------------------------
    from typing import Dict, Any
    def serialize_movie(movie: Movie) -> Dict[str, Any]:
        return {
            'id': movie.id,
            'title': movie.title,
            'tagline': movie.tagline,
            'category': movie.category,
            'rating_user': movie.rating_user,
            'middle_star': movie.middle_star,
        }
    # -----------------------------------
'''[v1]
class MovieDetailView(APIView):
    """ [GET] Вывод фильма """
    def get(self, request, pk):
        movie = Movie.objects.get(id=pk, draft=False)
        serializer = MovieDetailSerializer(movie)
        return Response(serializer.data)
'''
'''[v2]
class MovieDetailView(generics.RetrieveAPIView):
    """ [GET] Вывод фильма [9]"""
    queryset = Movie.objects.filter(draft=False)
    serializer_class = MovieDetailSerializer
'''
'''[v1]
class ReviewCreateView(APIView):
    """ [POST] Добавление комментария (к фильму) """
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)
'''
'''[v2]
class ReviewCreateView(generics.CreateAPIView):
    """ [POST] Добавление комментария (к фильму) [9]"""
    serializer_class = ReviewCreateSerializer
'''

"""###########################################################################
*ModelViewSet - позволяет нам реализ-ть сразу добавление, вывод списка, одной записи, обновления, удаления записи 
###########################################################################"""

class ReviewCreateViewSet(viewsets.ModelViewSet):
    """ [POST] Добавление комментария (к фильму) [14]"""
    serializer_class = ReviewCreateSerializer
'''[v1]
class AddStarRatingView(APIView):
    """[POST] Добавление рейтинга фильму """

    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)
'''
'''[v2]
class AddStarRatingView(generics.CreateAPIView):
    """[POST] Добавление рейтинга фильму """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        """ возвращает IP пользователя """
        serializer.save(ip=get_client_ip(self.request))
'''
class AddStarRatingViewSet(viewsets.ModelViewSet):
    """[POST] Добавление рейтинга фильму """
    serializer_class = CreateRatingSerializer

    def perform_create(self, serializer):
        """ возвращает IP пользователя """
        serializer.save(ip=get_client_ip(self.request))
'''[v1]
class ActorsListView(generics.ListAPIView):
    """ Вывод списка актёров [8] """
    queryset = Actor.objects.all()
    serializer_class = ActorListSelializer

class ActorsDetailView(generics.RetrieveAPIView):
    """ Вывод полного описания актёра / режжисёра [8] """
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSelializer
'''
class ActorsViewSet(viewsets.ReadOnlyModelViewSet):
    """" Вывод списка актёров [8] """
    queryset = Actor.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ActorListSelializer
        elif self.action == 'retrieve':
            return ActorDetailSelializer

#endregion