Certainly! Here's the Django model with the added `created_at` property:

```python
from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
  
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
```

To create a form, view, and HTML template for this model, you can follow the steps below:

1. Create a `forms.py` file in your Django app directory and define a form for the `Product` model:

```python
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name']
```


In your app's `urls.py` file, add the following code:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.create_product, name='create_product'),
]
```


2. In your `views.py` file, import the `ProductForm` and create a view to handle the form submission:

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ProductForm

def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully!')
            return redirect('create_product')  # Redirect to the create product page
    else:
        form = ProductForm()
    
    return render(request, 'create_product.html', {'form': form})

```

3. Create an HTML template named `create_product.html` in your app's template directory. Use HTML tags for the form without using Django's form rendering:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Create Product</title>
</head>
<body>
    <h1>Create Product</h1>
    {% if messages %}
        <ul class="messages">
            {% for message in messages %}
                <li {% if message.tags %} class="{{ message.tags }}"{% endif %}>
                    {{ message }}</li>
            {% endfor %}
        </ul>
    {% endif %}
    <form method="post">
        {% csrf_token %}
        <label for="id_name">Name:</label>
        <input type="text" name="name" id="id_name" required>
        <input type="submit" value="Create">
    </form>
</body>
</html>

```






---
---
---
## To update 





In your app's `urls.py` file, add the following URL pattern:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('product/create/', views.create_product, name='create_product'),
    path('product/update/<int:pk>/', views.update_product, name='update_product'),
]
```



In your `views.py` file, add the `update_product` view:

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import ProductForm
from .models import Product

def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully!')
            return redirect('update_product', pk=pk)  # Redirect to the same update product page
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'update_product.html', {'form': form, 'product': product})
```



In your HTML template, create a file named `update_product.html` and use the following code:

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Update Product</title>
  </head>
  <body>
    <h1>Update Product: {{ product.name }}</h1>
    {% if messages %}
    <ul class="messages">
      {% for message in messages %}
      <li {% if message.tags %} class="{{ message.tags }}" {% endif %}>
        {{ message }}</li>
      {% endfor %}
    </ul>
    {% endif %}
    <form method="post">
      {% csrf_token %}
      <label for="id_name">Name:</label>
      <input type="text" name="name" id="id_name"
        value="{{ form.instance.name }}" required>
      <input type="submit" value="Update">
    </form>
  </body>
</html>
```

