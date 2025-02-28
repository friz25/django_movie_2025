"""
СЕРИАЛИЗАТОРЫ - нужны чтоб приобразовывать типы данных python > в json (и наоборот)
"""
from rest_framework import serializers

from .models import Movie, Review, Rating, Actor
#-------*(попытка) Сериализация/Типизия/ДатаКлассы /чтоб pip Typing/Dataclasses--------------
from typing import Dict, Any

from django.contrib.auth.models import User


def serialize_user(user: User) -> Dict[str, Any]:
    return {
        'id': user.id,
        'last_login': user.last_login.isoformat() if user.last_login is not None else None,
        'is_superuser': user.is_superuser,
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'is_staff': user.is_staff,
        'is_active': user.is_active,
        'date_joined': user.date_joined.isoformat(),
    }
#-------------------------------------------------

class MovieListSerializer(serializers.Serializer):
    """ Список фильмов """
    id = serializers.IntegerField()
    title = serializers.CharField()
    tagline = serializers.CharField()
    category = serializers.CharField()
    rating_user = serializers.BooleanField()
    middle_star = serializers.IntegerField()

# class MovieListSerializer(serializers.ModelSerializer):
#     """ Список фильмов """
#     rating_user = serializers.BooleanField()
#     middle_star = serializers.IntegerField()
#
#     class Meta:
#         model = Movie
#         fields = ("id", "title", "tagline", "category", "rating_user", "middle_star")

class FilterReviewListSerializer(serializers.ListSerializer):
    """ Фильтр комментов, только parents """
    def to_representation(self, data):
        #тут data = наш queryset отзывов (мы фильтруем его и находим только те записи у которых parent=None)
        data = data.filter(parent=None)
        return super().to_representation(data)

class RecursiveSerializer(serializers.Serializer):
    """ Вывод рекурсивно children """
    def to_representation(self, value): #value = значение одной записи из БД
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data

class ActorListSelializer(serializers.ModelSerializer):
    """ Вывод списка актёров и режжисёров [8] """
    class Meta:
        model = Actor
        fields = ("id", "name", "image")

class ActorDetailSelializer(serializers.ModelSerializer):
    """ Вывод полного описания актёра и режжисёра [8] """
    class Meta:
        model = Actor
        fields = "__all__"

class ReviewCreateSerializer(serializers.ModelSerializer):
    """[POST] Добавление комментария (к фильму) """

    class Meta:
        model = Review
        fields = "__all__"

class ReviewSerializer(serializers.ModelSerializer):
    """[GET] Вывод комментария (к фильму) """
    children = RecursiveSerializer(many=True)

    class Meta:
        list_serializer_class = FilterReviewListSerializer
        model = Review
        fields = ("name", "text", "children")
        # fields = ("name", "text", "parent")

class MovieDetailSerializer(serializers.ModelSerializer):
    """ Полный фильмов """
    category = serializers.SlugRelatedField(slug_field="name", read_only=True)
    directors = ActorListSelializer(read_only=True, many=True)
    actors = ActorListSelializer(read_only=True, many=True)
    genres = serializers.SlugRelatedField(slug_field="name", read_only=True, many=True)
    reviews = ReviewSerializer(many=True)

    class Meta:
        model = Movie
        exclude = ("draft", )

class CreateRatingSerializer(serializers.ModelSerializer):
    """ Добавление рейтинга пользователем"""
    class Meta:
        model = Rating
        fields = ("star", "movie")

    def create(self, validated_data):
        rating, _ = Rating.objects.update_or_create(
            ip=validated_data.get('ip', None),
            movie=validated_data.get('movie', None),
            defaults={"star": validated_data.get('star')}
        )
        return rating