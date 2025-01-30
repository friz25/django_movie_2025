from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from .models import Actor, Movie, Genre
from .forms import ReviewForm


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
    queryset = Movie.objects.filter(draft=False) #вывести все кроме "черновиков"
    # template_name = "movies/movies.html"


# class MovieDetailView(View):
#     """Полное описание фильма"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {"movie": movie})

class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""
    model = Movie
    slug_field = 'url'

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
    def get_queryset(self):
        if 'genre' in self.request.GET and 'year' in self.request.GET:
            """Если выбраны и Жанр и Год"""
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")),
                Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct()
        else:
            queryset = Movie.objects.filter(
                Q(year__in=self.request.GET.getlist("year")) |
                Q(genres__in=self.request.GET.getlist("genre"))
            ).distinct()
        return queryset


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

