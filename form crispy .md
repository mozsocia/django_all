Bootstrap5 template pack for django-crispy-forms

## Installation

Install this plugin using `pip`:
```bash
$ pip install crispy-bootstrap5
```

## Usage

You will need to update your project's settings file to add ``crispy_forms``
and ``crispy_bootstrap5`` to your projects ``INSTALLED_APPS``. Also set
``bootstrap5`` as and allowed template pack and as the default template pack
for your project

```python
INSTALLED_APPS = (
    ...
    "crispy_forms",
    "crispy_bootstrap5",
    ...
)

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"

CRISPY_TEMPLATE_PACK = "bootstrap5"
```

in html template
```html
{% load crispy_forms_tags %}
<!DOCTYPE html>
<html>
<head>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.1/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-4bw+/aepP/YC94hEpVNVgiZdgIC5+VKNBQNGCHeKRQN+PtmoHDEXuppvnDJzQIu9" crossorigin="anonymous">
    <title>Add Blog</title>
</head>
<body>
    <h1>Add Blog</h1>
    <div class="container">
        <form method="post">
            {% csrf_token %}
            {{form|crispy}}
            <button type="submit">Save</button>
        </form>
        <a href="{% url 'blog_list' %}">Back to Blog List</a>
    </div>

</body>
</html>
```
