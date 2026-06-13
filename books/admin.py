from django.contrib import admin
from .models import Book, Author, Tag, Category

admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Category)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_at')
    search_fields = ('title', 'author', 'isbn')
    filter_horizontal = ('tags', 'categories')
