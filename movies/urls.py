from django.urls import path

from . import views


urlpatterns = [
    path("", views.MoviewView.as_view())
]