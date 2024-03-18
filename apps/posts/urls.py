# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    path('blogs/', blog_list, name='blog_list'),
    path('blogs/create/', blog_create, name='blog_create'),
    path('blogs/store/', blog_store, name='blog_store'),
    path('blogs/<int:blog_id>/show', blog_show, name='blog_show'),
    path('blogs/<int:blog_id>/edit/', blog_edit, name='blog_edit'),
    path('blogs/<int:blog_id>/update/', blog_update, name='blog_update'),
    path('blogs/<int:blog_id>/destroy/', blog_destroy, name='blog_destroy'),
]
