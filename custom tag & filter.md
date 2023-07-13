To make a database query and display the results using a custom tag in Django, you'll need to combine the use of a custom template tag with a Django model.

Here's an example of how you can achieve this:

1. Assuming you have a Django application with a model called `Product` representing your database table. Create a custom template tag to fetch and display the products.

In your `custom_tags.py` file, add the following code:

```python
from django import template
from your_app.models import Product

register = template.Library()

@register.simple_tag
def get_products():
    products = Product.objects.all()
    return products
```

2. In your Django template, load the custom tag library and use the custom tag to fetch and display the products:

```html
{% load custom_tags %}

<ul>
  {% get_products as product_list %}
  {% for product in product_list %}
    <li>{{ product.name }}</li>
  {% endfor %}
</ul>
```

In this example, we're using the custom tag `get_products` to fetch all the products from the `Product` model and store them in the `product_list` variable. We then iterate over the `product_list` and display the name of each product in an unordered list.

Ensure that you replace `your_app` with the actual name of your Django application containing the `Product` model. Additionally, you can modify the template code to suit your specific needs, such as displaying additional product details.

Remember to restart your Django server for the changes to take effect. The custom tag will query the database and retrieve the products whenever the template is rendered.

--------
----------
---------

Sure! Here's an example of a Django template filter that converts any output to a slug:

```python
from django import template
from django.utils.text import slugify

register = template.Library()

@register.filter
def slugify_filter(value):
    return slugify(value)

```

To use this filter in your Django templates, follow these steps:

1. Make sure you have created a Django app and added it to your project.
2. Create a file called `templatetags` in your app's directory if it doesn't exist.
3. Inside the `templatetags` directory, create a Python module file (e.g., `my_filters.py`).
4. Copy the code provided above into `my_filters.py`.
5. In your template, load the template tag library at the top using the `{% load %}` tag:

```django
{% load my_filters %}
```

6. Apply the `slugify_filter` to your desired output using the `|` (pipe) character:

```django
{{ some_variable|slugify_filter }}
```

For example, if you have a variable called `title` and want to display its slugified version, you would use:

```django
{{ title|slugify_filter }}
```

This filter will take the value of `title`, pass it through the `slugify_filter`, and display the resulting slug.
