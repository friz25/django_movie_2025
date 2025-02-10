from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from .models import Category, Genre, Movie, \
    MovieShots, Rating, RatingStar, Reviews, Actor


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label='Описание', widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    # """Категори"""
    # list_display = ("id", "name", "url")
    # list_display_links = ("name",)  # будет ссылкой (открытия записи)

    # ---- v2 ------
    """Категории"""
    # fields = ['name', 'rating']
    # exclude = ['slug']
    # readonly_fields = ['year']
    prepopulated_fields = {'url': ('name',)}
    # filter_horizontal = ['directors', 'actors', 'genres']
    # filter_vertical = ['actors']
    list_display = ['id', 'name', 'description']
    list_display_links = ['name']
    list_editable = ['description']
    # ordering = ['rating', 'name']
    list_per_page = 10
    # actions = ['set_dollars', 'set_euro']
    search_fields = ['name', 'description']  # + строка поиска
    # list_filter = ['title', 'year', 'country', 'budget', 'draft']  # +фильтры справа

class ReviewInLine(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ('parent', "name", "email")  # ток чтение / нельзя изменить (из админки)


class MovieShotsInLine(admin.TabularInline):
    """Кадры из фильма (на странице фильма)"""
    model = MovieShots
    extra = 1
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.image.url} width="140" height="100"')
        except:
            return ""

    get_image.short_description = "Изображение"


@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    """Фильмы"""
    # fields = ['name', 'rating']
    # exclude = ['slug']
    # prepopulated_fields = {'url': ('title', )}
    filter_horizontal = ['directors', 'actors', 'genres']
    # filter_vertical = ['actors']
    # ordering = ['rating', 'name']
    list_per_page = 10
    list_display = ('title', 'category', 'url', 'draft')
    list_filter = ('category', 'year')  # фильтр панеь (справа)
    search_fields = ('title', 'year', 'category__name')  # строка поиска
    inlines = [MovieShotsInLine, ReviewInLine] #список [комментов, кадров из фильма] к фильму
    save_on_top = True  # копия меню "сохранинь" (сверху)
    save_as = True  # можно создать новый фильм "редактируя прошлый"
    list_editable = ('year', 'country', 'budget', 'fees_in_usa', 'fees_in_world',) # из списка/каталога менять прям
    actions = ['publish', 'unpublish']
    form = MovieAdminForm #CKEditor
    readonly_fields = ('get_image',)
    # fields = (('actors', 'directors', 'genres'), )
    # чтоб поля в одну строку
    fieldsets = (
        (None, {
            "fields": (('title', 'tagline'),)
        }),
        (None, {
            "fields": (('description', ('poster', 'get_image'),))
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
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" height="140"')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запись была обновлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = 'Постер'


@admin.register(Reviews)
class ReviewAdmin(admin.ModelAdmin):
    # """Отзывы"""
    # list_display = ("name", 'email', 'parent', 'movie', 'id')
    # readonly_fields = ("name", "email")  # ток чтение / нельзя изменить (из админки)

    # ---- v2 ------
    """Отзывы"""
    # fields = ['name', 'rating']
    # exclude = ['parent']
    readonly_fields = ['parent', 'name', 'email'] # ток чтение / нельзя изменить (из админки)
    # prepopulated_fields = {'url': ('title',)}
    # filter_horizontal = ['movie']
    # filter_vertical = ['actors']
    list_display = ['name', 'email', 'text', 'parent', 'movie', 'id']
    list_editable = ['email', 'text', 'movie']
    # ordering = ['rating', 'name']
    list_per_page = 10
    # actions = ['set_dollars', 'set_euro']
    search_fields = ['name', 'text']  # + строка поиска
    # list_filter = ['title', 'year', 'country', 'budget', 'draft']  # +фильтры справа

@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    # """Жанры"""
    # list_display = ("name", 'url')

    #---- v2 ------
    """Жанры"""
    # fields = ['name', 'rating']
    # exclude = ['slug']
    # readonly_fields = ['year']
    prepopulated_fields = {'url': ('name',)}
    # filter_horizontal = ['directors', 'actors', 'genres']
    # filter_vertical = ['actors']
    list_display = ['name', 'description']
    list_editable = ['description']
    # ordering = ['rating', 'name']
    list_per_page = 10
    # actions = ['set_dollars', 'set_euro']
    search_fields = ['name', 'description']  # + строка поиска
    # list_filter = ['title', 'year', 'country', 'budget', 'draft']  #


@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    """Актёры"""
    list_display = ("name", 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.image.url} width="50" height="60"')
        except:
            return ""

    get_image.short_description = "Изображение"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("star", "movie", 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    """Кадры из фильма"""
    list_display = ("title", 'movie', 'get_image')
    readonly_fields = ('get_image',)

    def get_image(self, obj):
        try:
            return mark_safe(f'<img src={obj.image.url} width="100" height="60"')
        except:
            return ""

    get_image.short_description = "Изображение"


admin.site.register(RatingStar)

admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
