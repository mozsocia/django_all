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

urlpatterns = [
    path('create_sale/', views.create_sale, name='create_sale'),
]
```

```py
from django.shortcuts import render, redirect
from .models import Sales, SalesProduct

def create_sale(request):
    if request.method == 'POST':

        customer_name = request.POST['customer_name']
        location = request.POST['location']
        total_price = request.POST['total_price']
        
        sale = Sales.objects.create(customer_name=customer_name, location=location, total_price=total_price)
        
        product_names = request.POST.getlist('product_name[]')
        product_prices = request.POST.getlist('product_price[]')
        quantities = request.POST.getlist('quantity[]')
        
        for name, price, quantity in zip(product_names, product_prices, quantities):
            SalesProduct.objects.create(sales=sale, product_name=name, product_price=price, quantity=quantity)
        
        return redirect('create_sale')
    
    return render(request, 'create_sale.html')


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
    <input type="number" id="total_price" name="total_price"  required><br>

    <h2>Products:</h2>
    <div class="sales_products">
      <div class="single-product">
        <label >Product Name:</label><br>
        <input type="text"  name="product_name[]" required><br>

        <label >Product Price:</label><br>
        <input type="number"  name="product_price[]" required><br>

        <label >Quantity:</label><br>
        <input type="number" name="quantity[]" required><br><br>
      </div>
    </div>


    <button id="addProduct">Add Product</button> <br> <br>

    <input type="submit" value="Create Sale">

  </form>



  <script>
    document.addEventListener("DOMContentLoaded", function() {
        const addButton = document.getElementById("addProduct");
        const salesProductsDiv = document.querySelector(".sales_products");
  

        addButton.addEventListener("click", function() {
            const newProductDiv = document.createElement("div");
            newProductDiv.classList.add("single-product");
            newProductDiv.innerHTML = `
                <label>Product Name:</label><br>
                <input type="text" name="product_name[]" required><br>

                <label>Product Price:</label><br>
                <input type="number" name="product_price[]" step="0.01" required><br>

                <label>Quantity:</label><br>
                <input type="number" name="quantity[]" required><br><br>
            `;
            salesProductsDiv.appendChild(newProductDiv);

        });
    });
</script>
</body>

</html>
```
