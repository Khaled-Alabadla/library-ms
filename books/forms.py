from django import forms
from django.utils import timezone
from .models import Book, Tag, Category


class BookForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        help_text='Select one or more tags',
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-select'}),
        help_text='Select one or more categories',
    )
    # category = forms.ModelChoiceField(
    #     queryset=Book.objects.all(),
    #     empty_label='Choose category',
    #     widget=forms.Select(attrs={'class': 'form-control form-select'}),
    #     required=False,
    # )

    class Meta:
        model = Book
        fields = ['title', 'author', 'description', 'published_date', 'isbn', 'book_img']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'published_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'isbn': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        self.fields['author'].empty_label = None
        # populate tags and categories initial values when editing
        instance = kwargs.get('instance')
        if instance and instance.pk:
            self.fields['tags'].initial = instance.tags.all()
            self.fields['categories'].initial = instance.categories.all()

    def clean_title(self):
        title = self.cleaned_data.get('title', '')
        if not title or not title.strip():
            raise forms.ValidationError('Title cannot be blank.')
        return title
    
    def clean_published_date(self):
        published_date = self.cleaned_data.get('published_date')
        if published_date and published_date > timezone.now().date():
            raise forms.ValidationError('Published date cannot be in the future.')
        return published_date

    def clean_isbn(self):
        isbn = self.cleaned_data.get('isbn')
        if isbn:
            if len(isbn) < 10 or len(isbn) > 20:
                raise forms.ValidationError('ISBN should be between 10 and 20 characters.')
        return isbn

    def clean(self):
        cleaned = super().clean()
        errors = {}

        published_date = cleaned.get('published_date')
        if published_date and published_date > timezone.now().date():
            errors['published_date'] = 'Published date cannot be in the future.'

        isbn = cleaned.get('isbn')
        if isbn:
            if len(isbn) < 10 or len(isbn) > 20:
                errors['isbn'] = 'ISBN should be between 10 and 20 characters.'

        if errors:
            raise forms.ValidationError(errors)
        return cleaned

    def save(self, commit=True):
        # Save instance without committing m2m immediately so we can
        # handle assignments explicitly. Provide a save_m2m fallback
        # when commit=False so callers can call it later.
        instance = super().save(commit=False)

        tags_qs = self.cleaned_data.get('tags')
        cats_qs = self.cleaned_data.get('categories')

        if commit:
            instance.save()
            if tags_qs is not None:
                instance.tags.set(tags_qs)
            if cats_qs is not None:
                instance.categories.set(cats_qs)
            return instance

        # commit is False: attach a save_m2m method to the form instance
        def _save_m2m():
            if tags_qs is not None:
                instance.tags.set(tags_qs)
            if cats_qs is not None:
                instance.categories.set(cats_qs)

        # Ensure callers that expect ModelForm.save_m2m will work
        self.save_m2m = _save_m2m
        return instance
        

class ConfirmDeleteForm(forms.Form):
    confirm_title = forms.CharField(label='Type the book title to confirm', widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, book=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.book = book

    def clean_confirm_title(self):
        val = self.cleaned_data.get('confirm_title', '')
        if not self.book:
            raise forms.ValidationError('No book specified for confirmation.')
        if val.strip() != self.book.title:
            raise forms.ValidationError('Title does not match.')
        return val
