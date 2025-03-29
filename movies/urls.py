from django.contrib import admin
from django.urls import path
from rest_framework.routers import DefaultRouter # [14]
from rest_framework.urlpatterns import format_suffix_patterns # [14]

from . import views


urlpatterns = [
    path("", views.MoviesView.as_view()),
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("search/", views.Search.as_view(), name='search'),
    path("add-rating/", views.AddStarRating.as_view(), name='add_rating'),
    path("json-filter/", views.JsonFilterMoviesView.as_view(), name='json_filter'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),

    path('api/v1/upload/', views.S3FileUploadView.as_view(), name='upload_to_s3'), #[S3] http://127.0.0.1:8000/api/v1/upload/
]

urlpatterns += format_suffix_patterns([
    path("api/v1/movie/", views.MovieViewSet.as_view({'get': 'list'}, name='movies_list')), # http://127.0.0.1:8001/api/v1/movie/
    path("api/v1/movie/<int:pk>/", views.MovieViewSet.as_view({'get': 'retrieve'})), # http://127.0.0.1:8001/api/v1/movie/1
    # path("api/v1/movie/<int:pk>", views.MovieDetailView.as_view()),

    path("api/v1/review/", views.ReviewCreateViewSet.as_view({'post': 'create'})), # http://127.0.0.1:8001/api/v1/review/
    # path("api/v1/review/<int:pk>", views.ReviewDestroy.as_view()), #[17] кастомные права доступа

    path("api/v1/rating/", views.AddStarRatingViewSet.as_view({'post': 'create'})), # http://127.0.0.1:8001/api/v1/rating/ {"star":3, "movie": 1}
    # path("api/v1/actors/", views.ActorsListView.as_view()), # http://127.0.0.1:8001/api/v1/actors/
    # path("api/v1/actors/<int:pk>", views.ActorsDetailView.as_view()), # http://127.0.0.1:8001/api/v1/actors/1
    path("api/v1/actor/", views.ActorsViewSet.as_view({'get': 'list'})), # [14] http://127.0.0.1:8001/api/v1/actor/
    path("api/v1/actor/<int:pk>", views.ActorsViewSet.as_view({'get': 'retrieve'})), # [14] http://127.0.0.1:8001/api/v1/actor/1
    path("api/v1/actor/<int:pk>", views.ActorsViewSet.as_view({'get': 'retrieve'})), # [14] http://127.0.0.1:8001/api/v1/actor/1
    #================
    path("api/v1/profile/", views.ProfileViewSet.as_view({'get': 'list'}, name='profiles_list')), # http://127.0.0.1:8000/api/v1/profile/
    # path("api/v1/profile/<int:pk>/", views.ProfileViewSet.as_view({'get': 'retrieve', 'delete': 'delete', 'post': 'create'})), # http://127.0.0.1:8000/api/v1/profile/1
    path("api/v1/profile/<int:pk>/", views.ProfileViewSet.as_view({
        'get': 'retrieve',
        'delete': 'destroy',
        'post': 'create',
        'put': 'update',
        'patch': 'partial_update'
    })), # http://127.0.0.1:8000/api/v1/profile/1
    # path("api/v1/profile/", views.ProfileViewSet.as_view({'post': 'create'})), # http://127.0.0.1:8001/api/v1/profile/
    # path("api/v1/profile/<int:pk>/", views.ProfileViewSet.as_view({'delete': 'delete'})), # http://127.0.0.1:8001/api/v1/profile/

])




#####чтоб автогенерация url для наших классов: ########
# router = DefaultRouter()
# router.register(r'actor-set', api.ActorViewSet, basename='actor')
# router.register(r'actor-read', api.ActorReadOnly, basename='actor')
