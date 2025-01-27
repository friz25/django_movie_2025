from django.urls import path

from . import views


urlpatterns = [
    path("", views.MoviewView.as_view()),
    path("<int:pk>/", views.MovieDetailView.as_view()),
    # по сути 'pk' это id запрашиваемого фильма
]