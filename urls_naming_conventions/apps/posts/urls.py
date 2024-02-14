# urls.py
from django.urls import path
from .views import post_index, post_create, post_store, post_show, post_edit, post_update, post_destroy

urlpatterns = [
    # Read All
    path('posts/', post_index, name='post-index'),

    # Create
    path('posts/create/', post_create, name='post-create'),
    path('posts/store/', post_store, name='post-store'),

    # Read one
    path('posts/<int:post_id>/', post_show, name='post-show'),

    # Update
    path('posts/<int:post_id>/edit/', post_edit, name='post-edit'),
    path('posts/<int:post_id>/update/', post_update, name='post-update'),

    # Delete
    path('posts/<int:post_id>/destroy/', post_destroy, name='post-destroy'),
]
