# urls.py
from django.urls import path
from .views import *
from apps.posts import views


urlpatterns = [
    path('publishers/', views.publisher_list, name='publisher_list'),
    path('publishers/<int:pk>/', views.publisher_detail, name='publisher_detail'),
    path('authors/', views.author_list, name='author_list'),
    path('authors/<int:pk>/', views.author_detail, name='author_detail'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('tags/', views.tag_list, name='tag_list'),
    path('tags/<int:pk>/', views.tag_detail, name='tag_detail'),
]
