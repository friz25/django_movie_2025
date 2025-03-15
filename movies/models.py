from django.db import models
from datetime import date

from django.urls import reverse


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

    """возвращает абсолютный url // напр site.com/terminator/"""
    def get_absolute_url(self):
        return reverse("actor_detail", kwargs={"slug": self.name})

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

    """возвращает абсолютный url // напр site.com/terminator/"""
    def get_absolute_url(self):
        return reverse("movie_detail", kwargs={"slug": self.url})

    """возвращает (только) родительские отзывы к фильму"""
    def get_review(self):
        # return self.review_set.filter(parent__isnull=True)
        return self.reviews.filter(parent__isnull=True)
        """заменили 'review_set' на 'reviews' потому что в модели Reviews/поле movie
         указали related_name="reviews" """

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
        return f'{self.value}'

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звёзды рейтинга"
        ordering = ["-value"]


class Rating(models.Model):
    """Рейтинг"""
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="звезда")
    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        verbose_name="фильм",
        related_name="ratings" #по этому имени можем обращаться к данной таблице БД из таблицы Movie
    )

    """вернёт 'Количество звёзд - наз фильма' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return f"{self.star} - {self.movie}"

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"


class Review(models.Model):
    """Отзывы"""
    email = models.EmailField()
    name = models.CharField("Имя", max_length=100)
    text = models.TextField("Сообщение", max_length=5000)
    parent = models.ForeignKey(
        'self', verbose_name='Родитель', on_delete=models.SET_NULL, blank=True, null=True, related_name="children"
    )
    # 'self' потому что Отзыв будет ссылаться на Отзыв (на запись в этой же таблице)
    movie = models.ForeignKey(Movie, verbose_name="фильм", on_delete=models.CASCADE, related_name="reviews")

    """вернёт 'имя оставившего отзыв - наз фильма' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return f"{self.name} - {self.movie}"

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

from django.contrib.auth.models import User
from PIL import Image

class Profile(models.Model):
    GENDER_C = [
        ("Male", "Male"),
        ("Female", "Female"),
        ("Other", "Other")
    ]
    INTERESTS = [
        ("Harry Potter", "Harry Potter"),
        ("90s Kid", "90s Kid"),
        ("SoundCloud", "SoundCloud"),
        ("Spa", "Spa"),
        ("Self Care", "Self Care"),
        ("Heavy Metal", "Heavy Metal"),
        ("House Parties", "House Parties"),
        ("Gin tonic", "Gin tonic"),
        ("Gymnastics", "Gymnastics"),
        ("Hot Yoga", "Gymnastics"),
        ("Documentaries", "Documentaries"),
        ("Drama shows", "Drama shows"),
        ("Meditation", "Meditation"),
        ("Foodie", "Foodie"),
        ("Spotify", "Spotify"),
        ("Sushi", "Sushi"),
        ("Hockey", "Hockey"),
        ("Basketball", "Basketball"),
        ("Fantasy movies", "Fantasy movies"),
        ("Slam Poetry", "Slam Poetry"),
        ("Home Workout", "Home Workout"),
        ("Theater", "Theater"),
        ("Cafe hopping", "Cafe hopping"),
        ("Aquarium", "Aquarium"),
        ("Sneakers", "Sneakers"),
        ("Instagram", "Instagram"),
        ("Hot Springs", "Hot Springs"),
        ("Walking", "Walking"),
        ("Running", "Running"),
        ("Travel", "Travel"),
        ("Language Exchange", "Language Exchange"),
        ("Movies", "Movies"),
        ("Action movies", "Action movies"),
        ("Animated movies", "Animated movies"),
        ("Crime shows", "Crime shows"),
        ("Guitarists", "Guitarists"),
        ("Social Development", "Social Development"),
        ("Gym", "Gym"),
        ("Social Media", "Social Media"),
        ("Soul music", "Soul music"),
        ("Hip Hop", "Hip Hop"),
        ("Skincare", "Skincare"),
        ("Musical theater", "Musical theater"),
        ("J - Pop", "J - Pop"),
        ("Shisha", "Shisha"),
        ("Cricket", "Cricket"),
        ("Freelancing", "Freelancing"),
        ("Skateboarding", "Skateboarding")
    ]

    #region=== additional fields =======
    # SEXUAL_ORIENTATION = [
    #     ("Straight", "Straight"),
    #     ("Gay", "Gay"),
    #     ("Lesbian", "Lesbian"),
    #     ("Bisexual", "Bisexual"),
    #     ("Asexual", "Asexual"),
    #     ("Demisexual", "Demisexual"),
    #     ("Pansexual", "Pansexual"),
    #     ("Queer", "Queer")
    # ]
    # RELATIONSHIP_INTENT = [
    #     ("Long - term partner", "Long - term partner"),
    #     ("Long - term, open to short", "Long - term, open to short"),
    #     ("Short - term, open to long", "Short - term, open to long"),
    #     ("Short - term fun", "Short - term fun"),
    #     ("New friends", "New friends"),
    #     ("Still figuring it out", "Still figuring it out")
    # ]
    # MARITAL_STATUS = [
    #     ("Prefer not to answer", "Prefer not to answer"),
    #     ("It's complicated", "It's complicated"),
    #     ("Single", "Single"),
    #     ("Busy", "Busy")
    # ]
    # # What is your body type?
    # BODY_TYPE = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Атлетическое", "Атлетическое"),
    #     ("Среднее", "Среднее"),
    #     ("Пара лишних кило", "Пара лишних кило"),
    #     ("Крепкое", "Крепкое"),
    #     ("Приятная полнота", "Приятная полнота")
    # ]
    # HAIR_TYPE = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Черные", "Черные"),
    #     ("Светлые", "Светлые"),
    #     ("Каштановые", "Каштановые"),
    #     ("Окрашенные", "Окрашенные"),
    #     ("Немного седины", "Немного седины")
    # ]
    # EYES_COLOR = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Черные", "Черные"),
    #     ("Голубые", "Голубые"),
    #     ("Карие", "Карие"),
    #     ("Зеленые", "Зеленые"),
    #     ("Серые", "Серые")
    # ]
    # # Who do you live with?
    # ROOMMATE_STATUS = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Один", "Один"),
    #     ("В общежитии", "В общежитии"),
    #     ("С родителями", "С родителями"),
    #     ("Со второй половиной", "Со второй половиной"),
    #     ("С соседями", "С соседями")
    # ]
    # # What about children?
    # CHILDREN_STATUS = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Уже взрослые", "Уже взрослые"),
    #     ("Уже есть", "Уже есть"),
    #     ("Нет, никогда", "Нет, никогда"),
    #     ("Когда - нибудь", "Когда - нибудь")
    # ]
    # # What is your attitude towards smoking?
    # SMOKING_ATTITUDE = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Заядлый курильщик", "Заядлый курильщик"),
    #     ("Категорически против", "Категорически против"),
    #     ("Не курю", "Не курю"),
    #     ("Курю за компанию", "Курю за компанию"),
    #     ("Курю время от времени", "Курю время от времени")
    # ]
    # # What is your attitude towards alcohol?
    # ALCOHOL_ATTITUDE = [
    #     ("Предпочитаю не отвечать", "Предпочитаю не отвечать"),
    #     ("Выпиваю в компании", "Выпиваю в компании"),
    #     ("Не пью", "Не пью"),
    #     ("Не приемлю алкоголь", "Не приемлю алкоголь"),
    #     ("Много пью", "Много пью")
    # ]
    #endregion ===/additional fields =======

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField("Имя", max_length=100, null=True)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    gender = models.CharField(
        max_length=50, blank=True, null=True, choices=GENDER_C)
    profile_image = models.ImageField("Фото профиля юзера",
        upload_to='profile_pics/', default="default.jpg", null=True, blank=True)
    # About yourself
    description = models.TextField("Описание", null=True, blank=True)

    url = models.SlugField(max_length=130, unique=True)
    draft = models.BooleanField("Черновик", default=False)
    verified = models.BooleanField("Верифицирован", default=False)

    #region === additional fields =======
    # sexual_orientation = models.CharField(
    #     max_length=50, blank=True, null=True, choices=SEXUAL_ORIENTATION)
    # looking_for = models.CharField(
    #     max_length=50, blank=True, null=True, choices=RELATIONSHIP_INTENT) #RELATIONSHIP_INTENT
    # height = models.PositiveSmallIntegerField("Рост", default=0, blank=True)# What is your Height?
    # dont_show_height = models.BooleanField("Не показывать мой Рост", default=False)
    # weight = models.PositiveSmallIntegerField("Вес", default=0, blank=True)# What is your Weight?
    # dont_show_weight = models.BooleanField("Не показывать мой Вес", default=False)
    # marital_status = models.CharField(
    #     max_length=50, blank=True, null=True, choices=MARITAL_STATUS) # What is your marital status? Prefer not to answer / It's complicated / Single / Busy
    # body_type = models.CharField(
    #     max_length=50, blank=True, null=True, choices=BODY_TYPE) # What is your body type?
    # hair = models.CharField(
    #     max_length=50, blank=True, null=True, choices=HAIR_TYPE) # What is your hair colour?
    # eyes = models.CharField(
    #     max_length=50, blank=True, null=True, choices=EYES_COLOR) # What is your hair colour?
    #
    # roommate_status = models.CharField(
    #     max_length=50, blank=True, null=True, choices=ROOMMATE_STATUS) # Who do you live with?
    # children_status = models.CharField(
    #     max_length=50, blank=True, null=True, choices=CHILDREN_STATUS) # What about children?
    # smoking_attitude = models.CharField(
    #     max_length=50, blank=True, null=True, choices=SMOKING_ATTITUDE) # What is your attitude towards smoking?
    # alcohol_attitude = models.CharField(
    #     max_length=50, blank=True, null=True, choices=ALCOHOL_ATTITUDE) # What is your attitude towards alcohol?
    # working_at = models.CharField("Живу в", max_length=100, null=True, blank=True) # Where do you work / study?
    # studying_at = models.CharField("Живу в", max_length=100, null=True, blank=True) # Where do you work / study?
    # town_current = models.CharField("Живу в", max_length=100, null=True, blank=True) # Where do you live (town)?
    # town_from = models.CharField("Приехал(а) из", max_length=100, null=True, blank=True) # Where there you born / What town are you from ?
    #endregion ===/additional fields =======
    likeability = models.ManyToManyField(
        User, related_name="likes", blank=True)
    blocked_by = models.ManyToManyField(
        User, related_name="blocked", blank=True)

    """вернёт 'Юзер' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.full_name

    """возвращает абсолютный url // напр site.com/terminator/"""
    def get_absolute_url(self):
        return reverse("profile_detail", kwargs={"slug": self.url})

    def save(self, *args, **kwargs):
        """ Обрезать фото профиля юзера """
        super().save(*args, **kwargs)

        img = Image.open(self.profile_image.path)

        if img.height > 200 or img.width > 200:
            output_size = (250, 250)
            img.thumbnail(output_size)
            img.save(self.profile_image.path)

    @property
    def num_likes(self):
        """ возвращает кол-во лайков (поставленное юзером) """
        return self.likeability.all().count()

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Профиль юзера"
        verbose_name_plural = "Профили юзеров"

class ProfilePics(models.Model):
    """Фотки юзера"""
    title = models.CharField("Заголовок", max_length=100, null=True, blank=True)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ImageField("Фото юзера", upload_to="profile_pics/", null=True, blank=True)
    profile = models.ForeignKey(Profile, verbose_name="Профиль юзера", on_delete=models.CASCADE)

    """вернёт 'Title' вместо номера id='1' (удобней/наглядней) """
    def __str__(self):
        return self.title

    """то как таблица будет 'написана' в Админке"""
    class Meta:
        verbose_name = "Фотка юзера"
        verbose_name_plural = "Фотки юзера"