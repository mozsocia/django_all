# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .forms import BlogForm
from .models import Blog
from django.contrib import messages

@require_GET
def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'posts/blog_list.html', {'blogs': blogs})

@require_GET
def blog_create(request):
    form = BlogForm()
    return render(request, 'posts/add_blog.html', {'form': form})

@require_POST
def blog_store(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        blog = form.save()
        messages.success(request, 'Blog created successfully!')
        return redirect('blog_show', blog_id=blog.id)
    else:
        messages.error(request, 'Error creating blog. Please check the form.')
    return render(request, 'posts/add_blog.html', {'form': form})

@require_GET
def blog_show(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'posts/blog_show.html', {'blog': blog})

@require_GET
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(instance=blog)
    return render(request, 'posts/edit_blog.html', {'form': form, 'blog': blog})

@require_POST
def blog_update(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(request.POST,request.FILES, instance=blog)
    if form.is_valid():
        form.save()
        messages.success(request, 'Blog updated successfully!')
        return redirect('blog_show', blog_id=blog.id)
    else:
        messages.error(request, 'Error updating blog. Please check the form.')
    return render(request, 'posts/edit_blog.html', {'form': form, 'blog': blog})

@require_POST
def blog_destroy(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    messages.success(request, 'Blog deleted successfully!')
    return redirect('blog_list')