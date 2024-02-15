# views.py
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST, require_http_methods
from .forms import PostForm
from .models import Post

@require_GET
def post_index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})

@require_GET
def post_create(request):
    form = PostForm()
    return render(request, 'create.html', {'form': form})

@require_POST
def post_store(request):
    form = PostForm(request.POST)
    if form.is_valid():
        post = form.save()
        return redirect('post_show', post_id=post.id)
    return render(request, 'create.html', {'form': form})

@require_GET
def post_show(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    return render(request, 'show.html', {'post': post})

@require_GET
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(instance=post)
    return render(request, 'edit.html', {'form': form, 'post': post})

@require_http_methods(["PUT", "PATCH"])
def post_update(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = PostForm(request.POST, instance=post)
    if form.is_valid():
        form.save()
        return redirect('post_show', post_id=post.id)
    return render(request, 'edit.html', {'form': form, 'post': post})

@require_http_methods(["DELETE"])
def post_destroy(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post.delete()
    return redirect('post_index')
