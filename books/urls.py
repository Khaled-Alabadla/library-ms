from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('create/', views.book_create, name='create'),
    path('create/validate/', views.book_create_validate, name='create_validate'),
    path('<int:pk>/edit/', views.book_update, name='edit'),
    path('<int:pk>/delete/', views.book_delete, name='delete'),
    path('<int:pk>/ajax-delete/', views.book_delete_ajax, name='ajax_delete'),
]
