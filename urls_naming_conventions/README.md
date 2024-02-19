### Url Naming Conventions

**Models**
```python
# models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title
```

**forms**
```python
# forms.py
from django import forms
from .models import Blog

class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content']
```

**urls**
```python
# urls.py
from django.urls import path
from .views import *

urlpatterns = [
    # Read All
    path('blogs/', blog_index, name='blog_index'),

    # Create
    path('blogs/create/', blog_create, name='blog_create'),
    path('blogs/store/', blog_store, name='blog_store'),

    # Read one
    path('blogs/<int:blog_id>/', blog_show, name='blog_show'),

    # Update
    path('blogs/<int:blog_id>/edit/', blog_edit, name='blog_edit'),
    path('blogs/<int:blog_id>/update/', blog_update, name='blog_update'),

    # Delete
    path('blogs/<int:blog_id>/destroy/', blog_destroy, name='blog_destroy'),
]
```

**views**
```python
# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .forms import BlogForm
from .models import Blog

@require_GET
def blog_index(request):
    blogs = Blog.objects.all()
    return render(request, 'index.html', {'blogs': blogs})

@require_GET
def blog_create(request):
    form = BlogForm()
    return render(request, 'create.html', {'form': form})

@require_POST
def blog_store(request):
    form = BlogForm(request.POST)
    if form.is_valid():
        blog = form.save()
        return redirect('blog_show', blog_id=blog.id)
    return render(request, 'create.html', {'form': form})

@require_GET
def blog_show(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'show.html', {'blog': blog})

@require_GET
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(instance=blog)
    return render(request, 'edit.html', {'form': form, 'blog': blog})

@require_http_methods(["PUT", "PATCH"])
def blog_update(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(request.POST, instance=blog)
    if form.is_valid():
        form.save()
        return redirect('blog_show', blog_id=blog.id)
    return render(request, 'edit.html', {'form': form, 'blog': blog})

@require_http_methods(["DELETE"])
def blog_destroy(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    return redirect('blog_index')
```

These changes update the model, form, and view names to reflect the change from "Post" to "Blog." Make sure to update your templates and other references accordingly.
