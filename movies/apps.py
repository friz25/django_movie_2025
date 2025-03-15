from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'
    verbose_name = "Фильмы"

    # def ready(self): #[1] Profile
    #     import movies.signals
