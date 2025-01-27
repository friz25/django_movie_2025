from django.contrib import admin
from .models import Category, Genre, Movie, \
    MovieShots, Rating, RatingStar, Reviews, Actor


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("name",)  # будет ссылкой (открытия записи)


class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")  # ток чтение / нельзя изменить (из админки)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
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
    list_display = ("name", 'email', 'parent', 'movie', 'id')
    readonly_fields = ("name", "email")  # ток чтение / нельзя изменить (из админки)


admin.site.register(Genre)
admin.site.register(MovieShots)
admin.site.register(Actor)
admin.site.register(Rating)
admin.site.register(RatingStar)
