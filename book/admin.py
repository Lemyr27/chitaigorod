from django.contrib import admin
from book.models import Book, Author, Publisher, Genre, Language


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'year_published', 'publisher', 'downloads_count')
    list_display_links = ('title',)
    ordering = ('title',)
    search_fields = ('title', 'genre__name', 'year_published')
    list_filter = ['genre__name', 'publisher__name', 'languages__name']
    exclude = ('downloads_count',)
    filter_horizontal = ('languages', 'authors')


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'date_of_birth', 'date_of_death')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'date_foundation')
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = ('name',)
    ordering = ('name',)
    search_fields = ('name',)

