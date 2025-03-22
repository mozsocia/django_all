# urls.py
from django.urls import path
from .views import *
from apps.posts import views


urlpatterns = [
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/create/', blog_create, name='blog_create'),
    path('blogs/store/', blog_store, name='blog_store'),
    path('blogs/<int:blog_id>/show', blog_show, name='blog_show'),
    path('blogs/<int:blog_id>/edit/', blog_edit, name='blog_edit'),
    path('blogs/<int:blog_id>/update/', blog_update, name='blog_update'),
    path('blogs/<int:blog_id>/destroy/', blog_destroy, name='blog_destroy'),


    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('comments/', views.comment_list, name='comment_list'),
    path('comments/<int:pk>/', views.comment_detail, name='comment_detail'),
]
