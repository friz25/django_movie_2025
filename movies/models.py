from django.db import models
from datetime import date


class Category(models.Model):
    """ Категории """
    name = models.CharField("Категория", max_length=150)
    description = models.TextField("Описание", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)

    """вернёт 'Категория' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.name

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Actor(models.Model):
    """Актёры и Режиссёры"""
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ImageField("Изображение", upload_to='actors/')

    """вернёт 'Актёр' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.name

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Актёра и режиссёра"
        verbose_name_plural = "Актёры и режиссёры"


class Genre(models.Model):
    """Жанры"""
    name = models.CharField("Имя", max_length=100)
    description = models.TextField("Описание", null=True, blank=True)
    url = models.SlugField(max_length=160, unique=True)

    """вернёт 'Жанр' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.name

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"


class Movie(models.Model):
    """Фильм"""
    title = models.CharField("Название", max_length=100)
    tagline = models.CharField("Слоган", max_length=100, default='')
    description = models.TextField("Описание", null=True, blank=True)
    poster = models.ImageField("Постер", upload_to='movies/')
    year = models.PositiveSmallIntegerField("Дата выходы", default=2025)
    country = models.CharField("Страна", max_length=100)
    directors = models.ManyToManyField(Actor, verbose_name='режиссёр', related_name="film_director")
    actors = models.ManyToManyField(Actor, verbose_name='актёры', related_name="film_actor")
    genres = models.ManyToManyField(Genre, verbose_name='жанры')
    world_premiere = models.DateField("Премьера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField(
        "Сборы в США", default=0, help_text="указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField(
        "Сборы в мире", default=0, help_text="указывать сумму в долларах")
    category = models.ForeignKey(
        Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True
    )
    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    """вернёт 'Фильм' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.title

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class MovieShots(models.Model):
    """Кадры из фильма"""
    title = models.CharField("Заголовок", max_length=100)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, verbose_name="Фильм", on_delete=models.CASCADE)

    """вернёт 'Кадр' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.title

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Кадр из фильма"
        verbose_name_plural = "Кадры из фильма"


class RatingStar(models.Model):
    """Звезда рейтинга"""
    value = models.SmallIntegerField("Значение", default=0)

    """вернёт 'Количество звёзд' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.value

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="фильм")

    """вернёт 'Количество звёзд - наз фильма' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return f"{self.star} - {self.movie}"

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Reviews(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True
    )
    # 'self' потому что Отзыв будет ссылаться на Отзыв (на запись в этой же таблице)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE)

    """вернёт 'имя оставившего отзыв - наз фильма' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return f"{self.name} - {self.movie}"

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"
