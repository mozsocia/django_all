# models.py - Extended with more relations
from django.db import models

class Publisher(models.Model):
    name = models.CharField(max_length=100)
    founded_year = models.IntegerField()
    
    def __str__(self):
        return self.name

class Author(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, related_name='authors')
    birth_date = models.DateField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    published_date = models.DateField(null=True, blank=True)
    isbn = models.CharField(max_length=13, blank=True)
    
    def __str__(self):
        return self.title

class Chapter(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='chapters')
    title = models.CharField(max_length=100)
    number = models.IntegerField()
    
    def __str__(self):
        return f"{self.book.title} - Chapter {self.number}: {self.title}"

class Comment(models.Model):
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='comments')
    chapter = models.ForeignKey(Chapter, on_delete=models.SET_NULL, related_name='comments', null=True, blank=True)
    
    def __str__(self):
        return f"Comment on {self.book.title}: {self.content[:30]}..."

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    comments = models.ManyToManyField(Comment, related_name='tags')
    
    def __str__(self):
        return self.name