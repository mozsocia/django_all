Sure! Here's an example of how you can define models, serializers, views, and URLs for the given `Category` and `Book` models in Django with Django REST Framework (DRF):

**models.py:**

```python
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_title = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.book_title
```

**serializers.py:**

```python
from rest_framework import serializers
from .models import Category, Book

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class CategorySerializerGet(serializers.ModelSerializer):
    book_set = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = '__all__'

class BookSerializerGet(serializers.ModelSerializer):
    category = CategorySerializerGet()

    class Meta:
        model = Book
        fields = '__all__'
```

**views.py:**

```python
from rest_framework import generics
from .models import Category, Book
from .serializers import CategorySerializer, BookSerializer


class CategoryListCreateAPIView(APIView):
    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializerGet(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BookListCreateAPIView(APIView):
    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializerGet(books, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



```

**urls.py:**

```python
from django.urls import path
from .views import CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, \
    BookListCreateAPIView, BookRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('categories/', CategoryListCreateAPIView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyAPIView.as_view(), name='category-retrieve-update-destroy'),
    path('books/', BookListCreateAPIView.as_view(), name='book-list-create'),
    path('books/<int:pk>/', BookRetrieveUpdateDestroyAPIView.as_view(), name='book-retrieve-update-destroy'),
]
```

In the above code, we have defined two models, `Category` and `Book`, along with their corresponding serializers. The views are implemented using DRF's generic class-based views. We have separate views for listing, creating, retrieving, updating, and deleting both categories and books. The URLs are mapped to these views using Django's URL routing mechanism.

You can include these URLs in your project's main `urls.py` file by including `path('api/', include('your_app.urls'))` (replace `your_app` with the name of your Django app) to make them accessible under the `/api/` path.


# json data

Sure! Here are three example categories that you can use to post data in JSON format:

1. Category 1:
   ```json
   {
     "name": "Fiction"
   }
   ```

2. Category 2:
   ```json
   {
     "name": "Science Fiction"
   }
   ```

3. Category 3:
   ```json
   {
     "name": "Fantasy"
   }
   ```

You can use these JSON objects to create new categories by making a POST request to the corresponding endpoint in your Django application.

Certainly! Here are three examples of books that you can use to post data in JSON format:

1. Book 1:
   ```json
   {
     "book_title": "To Kill a Mockingbird",
     "category": 1
   }
   ```

2. Book 2:
   ```json
   {
     "book_title": "1984",
     "category": 2
   }
   ```

3. Book 3:
   ```json
   {
     "book_title": "Harry Potter and the Philosopher's Stone",
     "category": 3
   }
   ```

   Certainly! Here are six examples of books that you can use to post data in JSON format:

1. Book 1:
   ```json
   {
     "book_title": "The Great Gatsby",
     "category": 1
   }
   ```

2. Book 2:
   ```json
   {
     "book_title": "Pride and Prejudice",
     "category": 1
   }
   ```

3. Book 3:
   ```json
   {
     "book_title": "To Kill a Mockingbird",
     "category": 1
   }
   ```

4. Book 4:
   ```json
   {
     "book_title": "Harry Potter and the Sorcerer's Stone",
     "category": 2
   }
   ```

5. Book 5:
   ```json
   {
     "book_title": "The Hobbit",
     "category": 3
   }
   ```

6. Book 6:
   ```json
   {
     "book_title": "The Lord of the Rings: The Fellowship of the Ring",
     "category": 3
   }
   ```

In the above examples, the `category` field represents the foreign key relationship with the corresponding category. You can replace the numeric values with the actual primary key values of the categories in your database. Make sure to adjust the `category` field accordingly to match the primary key values of the desired categories when making a POST request to create the books.

In the above examples, the `category` field represents the foreign key relationship with the corresponding category. You can replace the numeric values with the actual primary key values of the categories in your database. Make sure to adjust the `category` field accordingly to match the primary key values of the desired categories when making a POST request to create the books.
