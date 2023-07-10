Certainly! Here's an example of how you can populate your Django database with sample data without using the Django-seed library. In this case, we'll modify the `myapp/seed_data.py` file.

Let's assume we have a Django app called "myapp" with a model called "Product" that has the following fields:

```python
# myapp/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

To seed the "Product" model with some sample data, create a new file called "seed_data.py" within your app directory.



```python
# myapp/seed_data.py
import random
import string
from django.utils import timezone
from myapp.models import Product

def generate_random_string(length):
    """Helper function to generate a random string of specified length."""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def load_data():
    for _ in range(10):
        product = Product(
            name=generate_random_string(10),
            price=random.randint(10, 100),
            description=generate_random_string(50),
            created_at=timezone.now()
        )
        product.save()
    print("Seeded 10 products.")
```

In this example, we define a helper function `generate_random_string` to generate a random string of a specified length using lowercase and uppercase letters. Then, within the `load_data` function, we loop 10 times to create and save instances of the `Product` model with random data for the `name`, `price`, `description`, and `created_at` fields.

To execute the seed data, you can use a management command similar to the previous example:

```python
# myapp/management/commands/seed_db.py
from django.core.management.base import BaseCommand
from myapp.seed_data import load_data

class Command(BaseCommand):
    help = 'Seeds the database with sample data.'

    def handle(self, *args, **options):
        load_data()
```

Finally, run the management command to seed your database:

```
python manage.py seed_db
```

This will populate your "Product" model with 10 randomly generated records, just like the previous example.

Remember to update the import paths and adjust the fields and number of records as per your requirements.
