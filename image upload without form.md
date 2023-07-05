Sure! Here's a Django app for the given `Image` model:
**models.py**
```python
class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
```

**urls.py**
```python
from django.urls import path
from . import views

app_name = 'image_app'

urlpatterns = [
    path('', views.image_list, name='image_list'),
    path('upload/', views.image_upload, name='image_upload'),
]
```

**views.py**
```python
from django.shortcuts import render, redirect
from .models import Image

def image_list(request):
    images = Image.objects.all()
    return render(request, 'image_list.html', {'images': images})

def image_upload(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        image_file = request.FILES.get('image')
        Image.objects.create(title=title, image=image_file)
        return redirect('image_list')
    
    return render(request, 'image_upload.html')
```

**image_list.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Image List</title>
</head>
<body>
    <h1>Image List</h1>
    <ul>
        {% for image in images %}
            <li>
                <h3>{{ image.title }}</h3>
                <img src="{{ image.image.url }}" alt="{{ image.title }}" width="300">
                <p>Uploaded at: {{ image.uploaded_at }}</p>
            </li>
        {% empty %}
            <li>No images found.</li>
        {% endfor %}
    </ul>
    <a href="{% url 'image_upload' %}">Upload Image</a>
</body>
</html>
```

**image_upload.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Image Upload</title>
</head>
<body>
    <h1>Image Upload</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <label for="id_title">Title:</label>
        <input type="text" name="title" id="id_title" required><br><br>
        <label for="id_image">Image:</label>
        <input type="file" name="image" id="id_image" required><br><br>
        <input type="submit" value="Upload">
    </form>
    <a href="{% url 'image_list' %}">Back to Image List</a>
</body>
</html>
```

In this example, we have two views: `image_list` and `image_upload`. The `image_list` view retrieves all the `Image` objects from the database and renders them in the `image_list.html` template. The `image_upload` view handles the image upload form submission and creates a new `Image` object with the provided title and image file.

The HTML templates use Django template tags to dynamically render the images and URLs. The `image_list.html` template displays a list of images with their titles, uploaded dates, and a link to upload a new image. The `image_upload.html` template displays a form to upload a new image with a title and file input field.

Remember to configure your Django project's `urls.py` to include this app's URLs and also ensure that you have properly set up your media file handling in your Django settings.


---
---

Certainly! Here's an updated version of the Django app that uses a `forms.Form` to validate the input:

**forms.py**
```python
from django import forms

class ImageUploadForm(forms.Form):
    title = forms.CharField(max_length=255)
    image = forms.ImageField()
```

**views.py**
```python
from django.shortcuts import render, redirect
from .forms import ImageUploadForm
from .models import Image


def image_upload(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            image_file = form.cleaned_data['image']
            Image.objects.create(title=title, image=image_file)
            return redirect('image_app:image_list')
    else:
        form = ImageUploadForm()
    
    return render(request, 'image_app/image_upload.html', {'form': form})
```

**image_upload.html**
```html
<!DOCTYPE html>
<html>
<head>
    <title>Image Upload</title>
</head>
<body>
    <h1>Image Upload</h1>
    <form method="post" enctype="multipart/form-data">
        {% csrf_token %}
        <label for="id_title">Title:</label>
        <input type="text" name="title" id="id_title" required><br><br>
        <label for="id_image">Image:</label>
        <input type="file" name="image" id="id_image" required><br><br>
        <input type="submit" value="Upload">
    </form>
    <a href="{% url 'image_list' %}">Back to Image List</a>
</body>
</html>

```




----
---



To set the `MEDIA_ROOT` and `MEDIA_URL` in Django, follow these steps:

1.  Open your project's settings file (`settings.py`).
    
2.  Add the following lines at the top of the file to import the necessary modules:
    
    ```py
    import os
    from django.urls import reverse_lazy
    
    ```
    
3.  Locate the existing `STATIC_URL` setting, and below it, add the following lines to set the `MEDIA_ROOT` and `MEDIA_URL`:
    
    ```
    # Base directory for uploaded media files
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
    
    # URL prefix for media files
    MEDIA_URL = '/media/'
    
    ```
    
    In this example, the `MEDIA_ROOT` is set to a directory called `'media'` located in your project's base directory. The `MEDIA_URL` is set to `'/media/'`, which will serve media files from the specified directory.
    
4.  Save the changes to `settings.py`.
    
5.  In your project's main `urls.py` file, add the following lines at the top to import the necessary modules:
    
    ```
    from django.conf import settings
    from django.conf.urls.static import static
    
    ```
    
6.  Locate the `urlpatterns` list and modify it as shown below to include the media URL configuration:
    
    ```
    urlpatterns = [
        # ...existing URL patterns...
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    ```
    
    The `static` function is used to serve static files during development, and in this case, it is also used to serve media files by adding the `MEDIA_URL` and `MEDIA_ROOT` settings.
