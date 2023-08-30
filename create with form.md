```py

from django.db import models

class Sales(models.Model):
    customer_name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Sale by {self.customer_name} at {self.location}"

class SalesProduct(models.Model):
    sales = models.ForeignKey(Sales, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=100)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity}x {self.product_name} in sale {self.sales}"
```

```py
from django import forms
from .models import Sales, SalesProduct

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields = ['customer_name', 'location', 'total_price']

class SalesProductForm(forms.ModelForm):
    class Meta:
        model = SalesProduct
        fields = ['product_name', 'product_price', 'quantity']

```

```py

urlpatterns = [
    path('create_sale/', views.create_sale, name='create_sale'),
]
```
==============
### views.py
```py

from django.shortcuts import render, redirect
from .forms import SalesForm, SalesProductForm
from .models import Sales, SalesProduct

def create_sale(request):

    if request.method == 'POST':
        sales_products_count = int(request.POST['sales_products_count'])
        sales_form = SalesForm(request.POST)
        product_forms = [SalesProductForm(request.POST, prefix=str(i)) for i in range(sales_products_count)]

        if sales_form.is_valid() and all(form.is_valid() for form in product_forms):
            sale = sales_form.save()

            for form in product_forms:
                product = form.save(commit=False)
                product.sales = sale
                product.save()

            return redirect('create_sale')
    else:
        sales_form = SalesForm()
        product_forms = SalesProductForm()

    return render(request, 'create_sale.html', {'sales_form': sales_form, 'product_forms': product_forms})


```

### create_sale.html
```html
<!DOCTYPE html>
<html>

<head>
    <title>Create Sale</title>
</head>

<body>
    <h1>Create Sale</h1>
    <form method="post">
        {% csrf_token %}

        <label for="customer_name">Customer Name:</label><br>
        <input type="text" id="customer_name" name="customer_name" required><br>

        <label for="location">Location:</label><br>
        <input type="text" id="location" name="location" required><br>

        <label for="total_price">Total Price:</label><br>
        <input type="number" id="total_price" name="total_price" step="0.01" required><br>

        <h2>Products:</h2>
        <div class="sales_products">
            <input type="hidden" name="sales_products_count" value="2"><br>
            <div class="single-product">
                <label>Product Name:</label><br>
                <input type="text" name="0-product_name" required><br>

                <label>Product Price:</label><br>
                <input type="number" name="0-product_price"  required><br>

                <label>Quantity:</label><br>
                <input type="number" name="0-quantity" required><br><br>
            </div>
            <div class="single-product">
                <label>Product Name:</label><br>
                <input type="text" name="1-product_name" required><br>

                <label>Product Price:</label><br>
                <input type="number" name="1-product_price"  required><br>

                <label>Quantity:</label><br>
                <input type="number" name="1-quantity" required><br><br>
            </div>
            
        </div>
        <button id="addProduct">Add Product</button><br><br>
        <input type="submit" value="Create Sale">
    </form>

    <script>
        document.addEventListener("DOMContentLoaded", function() {
            const addButton = document.getElementById("addProduct");
            const salesProductsDiv = document.querySelector(".sales_products");
            const countInput = document.querySelector('input[name="sales_products_count"]');
            let productCount = parseInt(countInput.value);

            addButton.addEventListener("click", function() {
                const newProductDiv = document.createElement("div");
                newProductDiv.classList.add("single-product");
                newProductDiv.innerHTML = `
                    <label>Product Name:</label><br>
                    <input type="text" name="${productCount}-product_name" required><br>

                    <label>Product Price:</label><br>
                    <input type="number" name="${productCount}-product_price"  required><br>

                    <label>Quantity:</label><br>
                    <input type="number" name="${productCount}-quantity" required><br><br>
                `;
                salesProductsDiv.appendChild(newProductDiv);

                productCount++;
                countInput.value = productCount.toString();
            });
        });
    </script>
</body>

</html>
```
