from django import template
from movies.models import Category, Movie

register = template.Library() # для регистрации наших тегов (в django)

@register.simple_tag() # этот декоратор позволит зарегать наш тег (в django)
def get_categories():
    """Вывод всех категорий"""
    return Category.objects.all()

@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    """Возвращает последние 5 добавл фильмов"""
    movies = Movie.objects.order_by("id")[:count]
    return {'last_movies': movies}
