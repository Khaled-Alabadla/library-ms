from django.contrib import admin
from .models import Book, Author

admin.site.register(Author)

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date', 'created_at')
    search_fields = ('title', 'author', 'isbn')
