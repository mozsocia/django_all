from django.db import models

class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title


# In your models.py
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    # ForeignKey to Book (many Comments can belong to one Book)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    
    # Optional: if you want to track who made the comment
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f"Comment on {self.book.title}: {self.content[:30]}..."