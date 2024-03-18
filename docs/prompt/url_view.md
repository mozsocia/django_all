
for djnago , give me urls, views like below template for "CustomUser" model

```py
class blog(AbstractBaseUser, PermissionsMixin):
    title = models.CharField(max_length=255)
    content = models.CharField(max_length=100, unique=True)
    points = models.IntegerField( default = 0)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    referral = models.ForeignKey('self', blank=True, null=True, on_delete=models.SET_NULL,)
    otp = models.CharField(max_length=10, blank=True, null=True)
    email = models.EmailField(unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='users_images', blank=True, null=True, verbose_name='Profile Image')
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_reseller = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    accept_terms = models.BooleanField(verbose_name='Accept all the Terms & Conditions', default=False)

```


**urls**
```python
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
```

**views**
```python
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
    return render(request, 'blog_list.html', {'blogs': blogs})

@require_GET
def blog_create(request):
    form = BlogForm()
    return render(request, 'add_blog.html', {'form': form})

@require_POST
def blog_store(request):
    form = BlogForm(request.POST, request.FILES)
    if form.is_valid():
        blog = form.save()
        messages.success(request, 'Blog created successfully!')
        return redirect('blog_show', blog_id=blog.id)
    else:
        messages.error(request, 'Error creating blog. Please check the form.')
    return render(request, 'add_blog.html', {'form': form})

@require_GET
def blog_show(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    return render(request, 'blog_show.html', {'blog': blog})

@require_GET
def blog_edit(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    form = BlogForm(instance=blog)
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})

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
    return render(request, 'edit_blog.html', {'form': form, 'blog': blog})

@require_POST
def blog_destroy(request, blog_id):
    blog = get_object_or_404(Blog, pk=blog_id)
    blog.delete()
    messages.success(request, 'Blog deleted successfully!')
    return redirect('blog_list')
```