# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Read All
    path('posts/', post_index, name='post_index'),

    # Create
    path('posts/create/', post_create, name='post_create'),
    path('posts/store/', post_store, name='post_store'),

    # Read one
    path('posts/<int:post_id>/', post_show, name='post_show'),

    # Update
    path('posts/<int:post_id>/edit/', post_edit, name='post_edit'),
    path('posts/<int:post_id>/update/', post_update, name='post_update'),

    # Delete
    path('posts/<int:post_id>/destroy/', post_destroy, name='post_destroy'),
]
