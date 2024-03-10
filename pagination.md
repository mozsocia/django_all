**Models**
```py
# models.py
from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()


```


**urls**
```py
# urls.py
from django.urls import path
from .views import blog_list

urlpatterns = [
    path('blogs/', blog_list, name='blog_list'),
]

```


**views**
```py
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from .models import Blog

def blog_list(request):
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list, 5)  # Show 5 blogs per page

    page = request.GET.get('page')
    try:
        blogs = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        blogs = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        blogs = paginator.page(paginator.num_pages)

    return render(request, 'blog/blog_list.html', {'blogs': blogs})
```

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Blog List</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css">
</head>

<body>

    <div class="container mt-5">
        <h1>Blog List</h1>
        <ul class="list-group">
            {% for blog in blogs %}
            <li class="list-group-item">
                <h3>{{ blog.title }}</h3>
                <p>{{ blog.content }}</p>
            </li>
            {% endfor %}
        </ul>

        <div class="pagination mt-3">
            <ul class="pagination">

                {% if blogs.has_previous %}
                <li class="page-item">
                    <a class="page-link" href="?page=1" aria-label="First"> &laquo; first </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ blogs.previous_page_number }}" aria-label="Previous"> previous </a>
                </li>
                {% endif %}

                <li class="page-item disabled">
                    <span class="page-link current"> Page {{ blogs.number }} of {{ blogs.paginator.num_pages }}. </span>
                </li>

                {% if blogs.has_next %}
                <li class="page-item">
                    <a class="page-link" href="?page={{ blogs.next_page_number }}" aria-label="Next"> next </a>
                </li>
                <li class="page-item">
                    <a class="page-link" href="?page={{ blogs.paginator.num_pages }}" aria-label="Last"> last &raquo; </a>
                </li>
                {% endif %}

            </ul>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>

</html>
```
