from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class BookManager(models.Manager):
    def create_book(self, data):
        title = data.get('title').strip()
        author = data.get('author').strip()
        description = data.get('description').strip()
        published_date = data.get('published_date')
        isbn = data.get('isbn').strip()
        self.create(title = title, author = author, description = description, published_date = published_date, isbn = isbn)
        return self

    def update_book(self, book, data):
        # Simple updater: assign known fields and save.
        fields = ['title', 'author', 'description', 'published_date', 'isbn', 'book_img']
        for field in fields:
            if field in data:
                setattr(book, field, data[field])
        book.save(using=self._db)
        # Note: tags handling is done in the form save method to avoid
        # circular imports and to ensure proper creation of Tag objects.
        return book
    
class Author(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="books")
    description = models.TextField(blank=True)
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    book_img = models.ImageField(upload_to='images/', null=True, blank=True)
    tags = models.ManyToManyField('Tag', blank=True, related_name='books')
    categories = models.ManyToManyField('Category', blank=True, related_name='books')


    objects = BookManager()

    def __str__(self):
        return f"{self.title} by {self.author}"


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
