To use CKEditor for form input fields in HTML and save them in a Django model field without using any libraries or Django forms, you can follow these steps:

1. Install CKEditor: Download the CKEditor library from the official website (https://ckeditor.com/ckeditor-4/) and extract the files. Place the CKEditor folder in your project's static files directory.

2. Create a Django model: Open your Django app's `models.py` file and create a model that includes a field to store the CKEditor content. For example:

```python
from django.db import models

class MyModel(models.Model):
    content = models.TextField()
```

3. Create the necessary routes: Open your app's `urls.py` file and define the necessary URL routes for reading and creating instances of the model. For example:

```python
from django.urls import path
from . import views

app_name = 'myapp'

urlpatterns = [
    path('', views.my_model_list, name='my_model_list'),
    path('create/', views.my_model_create, name='my_model_create'),
]
```

4. Define the views: Open your app's `views.py` file and define the views for reading and creating instances of the model. For example:

```python
from django.shortcuts import render, redirect
from .models import MyModel

def my_model_list(request):
    my_models = MyModel.objects.all()
    return render(request, 'my_model_list.html', {'my_models': my_models})

def my_model_create(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        MyModel.objects.create(content=content)
        return redirect('my_model_list')
    return render(request, 'my_model_create.html')
```

5. Create the HTML templates: Create two HTML templates, `my_model_list.html` and `my_model_create.html`, inside a `templates/myapp` directory. 

`my_model_list.html` example:
```html
{% for my_model in my_models %}
    <div>{{ my_model.content|safe }}</div>
{% empty %}
    <p>No models found.</p>
{% endfor %}
```

`my_model_create.html` example:
```html
<form method="POST" action="{% url 'my_model_create' %}">
    {% csrf_token %}
    <textarea name="content" class="ckeditor" rows="10" cols="80"></textarea>
    <button type="submit">Create</button>
</form>

<script src="https://cdn.ckeditor.com/4.22.1/standard/ckeditor.js"></script>
<script>
    CKEDITOR.replace('ckeditor');
</script>
```

Note: In the `my_model_create.html` template, the CKEditor script is loaded using the `{% static %}` template tag assuming you have configured static files correctly in your Django project.

That's it! With these steps, you can use CKEditor in your HTML form to input content and save it to the `content` field of your `MyModel` model.
