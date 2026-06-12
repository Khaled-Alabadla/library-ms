from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from .models import Book
from .forms import BookForm, ConfirmDeleteForm
from accounts.utils import is_logged_in


def dashboard(request):
    if not is_logged_in:
        return redirect('login')
    books = Book.objects.order_by('-created_at')
    return render(request, 'books/dashboard.html', {'books': books})


def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST,  request.FILES)
        if form.is_valid():
            form.save()
            # Book.objects.create_book(form.cleaned_data)
            messages.success(request, 'Book created successfully.')
            return redirect('books:dashboard')
    else:
        form = BookForm()
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Create'})


def book_create_validate(request):
    """AJAX endpoint to validate the create form without creating the object.

    Returns JSON: {'success': True} when valid, or {'success': False, 'errors': {...}}
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    # Accept files as well; return JSON-ready errors using Django API
    form = BookForm(request.POST, request.FILES)
    if form.is_valid():
        return JsonResponse({'success': True})
    # form.errors.get_json_data() returns a JSON-serializable structure
    # Build a mapping of field -> [messages] so the client can show errors per-field
    json_data = form.errors.get_json_data()
    errors = {field: [err['message'] for err in err_list] for field, err_list in json_data.items()}
    return JsonResponse({'success': False, 'errors': errors})


def book_update(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            # Use manager to update (pass instance and cleaned data)
            form.save()
            messages.success(request, 'Book updated successfully.')
            return redirect('books:dashboard')
    else:
        form = BookForm(instance=book)
    return render(request, 'books/book_form.html', {'form': form, 'action': 'Update'})


def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        form = ConfirmDeleteForm(request.POST, book=book)
        if form.is_valid():
            book.delete()
            messages.success(request, 'Book deleted.')
            return redirect('books:dashboard')
    else:
        form = ConfirmDeleteForm(book=book)
    return render(request, 'books/book_confirm_delete.html', {'form': form, 'book': book})


def book_delete_ajax(request, pk):
    """Handle AJAX delete requests for a Book. Returns JSON."""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method.'}, status=405)

    book = get_object_or_404(Book, pk=pk)
    try:
        book.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
