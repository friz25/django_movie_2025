from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, \
    MovieShots, Rating, RatingStar, Reviews, Actor


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категори"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)  # будет ссылкой (открытия записи)


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")  # ток чтение / нельзя изменить (из админки)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')  # фильтр панеь (справа)
    search_fields = ('title', 'category__name')  # строка поиска
    inlines = [ReviewInLine]
    save_on_top = True  # копия меню "сохранинь" (сверху)
    save_as = True  # можно создать новый фильм "редактируя прошлый"
    list_editable = ("draft",)  # из списка/каталога менять прям
    # fields = (('actors', 'directors', 'genres'), )
    fieldsets = (
        (None, {
            "fields": (('title', 'tagline'),)
        }),
        (None, {
            "fields": (('description', 'poster'),)
        }),
        (None, {
            "fields": (('year', 'world_premiere', 'country'),)
        }),
        ("Actors", {
            "classes": ("collapse",),
            "fields": (('actors', 'directors', 'genres', 'category'),)
        }),
        (None, {
            "fields": (('budget', 'fees_in_usa', 'fees_in_world'),)
        }),
        ("Options", {
            "fields": (('url', 'draft'),)
        }),
    )  # чтоб поля в одну строку


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", 'email', 'parent', 'movie', 'id')
    readonly_fields = ("name", "email")  # ток чтение / нельзя изменить (из админки)

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", 'url')

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Актёры"""
    list_display = ("name", 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60"')

    get_image.short_description = "Изображение"

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", 'ip')

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", 'movie')

admin.site.register(RatingStar)
