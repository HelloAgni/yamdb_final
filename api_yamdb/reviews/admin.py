from django.contrib import admin
from django.db.models import Avg

from .models import Category, Comment, Genre, Review, Title, User

EMPTY_VALUE = '-пусто-'


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'username', 'bio', 'role', 'email', 'first_name', 'last_name'
    )
    search_fields = ('username',)
    list_filter = ('username', 'role')
    empty_value_display = EMPTY_VALUE


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = EMPTY_VALUE


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'review', 'author', 'text', 'pub_date')
    search_fields = ('author', 'text')
    list_filter = ('author', 'text')
    empty_value_display = EMPTY_VALUE


class GenreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    search_fields = ('name', 'slug')
    list_filter = ('name', 'slug')
    empty_value_display = EMPTY_VALUE


class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'title', 'author', 'text', 'score', 'pub_date'
    )
    search_fields = ('author', 'title', 'pub_date')
    list_filter = ('author', 'title', 'pub_date')
    empty_value_display = EMPTY_VALUE


class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'name', 'year', 'category', 'description', 'rating'
    )
    search_fields = ('name', 'year', 'category', 'genre')
    list_filter = ('name', 'year', 'category', 'genre')
    empty_value_display = EMPTY_VALUE
    readonly_fields = ('rating',)

    def rating(self, instance):
        return Review.objects.filter(title=instance).aggregate(Avg('score'))

    rating.short_description = 'Рейтинг'


admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Title, TitleAdmin)
