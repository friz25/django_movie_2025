from django.shortcuts import redirect, render
from django.views.generic import DetailView, ListView
from django.views.generic.base import View

from .models import Movie
from .forms import ReviewForm

# Старый вид/класс / записан через View()
# class MoviesView(View):
#     """Список фильмов"""
#     def get(self, request):
#         movies = Movie.objects.all()
#         return render(request, "movies/movies.html", {"movie_list": movies})

class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False) #вывести все кроме "черновиков"
    # template_name = "movies/movies.html"


# class MovieDetailView(View):
#     """Полное описание фильма"""
#     def get(self, request, slug):
#         movie = Movie.objects.get(url=slug)
#         return render(request, 'movies/movie_detail.html', {"movie": movie})

class MovieDetailView(DetailView):
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
                form.movie = movie
                form.save() # записываем (данные из формы) в БД
            return redirect(movie.get_absolute_url()) #напр на эту же / обновляет страницу
