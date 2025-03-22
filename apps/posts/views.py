# views.py
from django.http import JsonResponse
from .models import Publisher, Author, Book, Chapter, Comment, Tag
from .serializers import serialize_queryset_to_list, serialize_instance_to_dict

# Publisher views with 4 levels of nesting
def publisher_list(request):
    publishers = Publisher.objects.all()
    data = serialize_queryset_to_list(publishers, include_relations=[
        'authors', 
        'authors.books', 
        'authors.books.chapters', 
        'authors.books.comments'
    ])
    return JsonResponse(data, safe=False)

def publisher_detail(request, pk):
    try:
        publisher = Publisher.objects.get(pk=pk)
        data = serialize_instance_to_dict(publisher, include_relations=[
            'authors', 
            'authors.books', 
            'authors.books.chapters', 
            'authors.books.comments',
            'authors.books.comments.tags'  # 5th level!
        ])
        return JsonResponse(data)
    except Publisher.DoesNotExist:
        return JsonResponse({'error': 'Publisher not found'}, status=404)

# Author views
def author_list(request):
    authors = Author.objects.all()
    data = serialize_queryset_to_list(authors, include_relations=[
        'publisher',
        'books', 
        'books.chapters', 
        'books.comments'
    ])
    return JsonResponse(data, safe=False)

def author_detail(request, pk):
    try:
        author = Author.objects.get(pk=pk)
        data = serialize_instance_to_dict(author, include_relations=[
            'publisher',
            'books', 
            'books.chapters', 
            'books.comments',
            'books.comments.tags'
        ])
        return JsonResponse(data)
    except Author.DoesNotExist:
        return JsonResponse({'error': 'Author not found'}, status=404)

# Book views
def book_list(request):
    books = Book.objects.all()
    data = serialize_queryset_to_list(books, include_relations=[
        'author',
        'author.publisher',
        'chapters',
        'comments',
        'comments.chapter'
    ])
    return JsonResponse(data, safe=False)

def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
        data = serialize_instance_to_dict(book, include_relations=[
            'author',
            'author.publisher',
            'chapters',
            'comments',
            'comments.chapter',
            'comments.tags'
        ])
        return JsonResponse(data)
    except Book.DoesNotExist:
        return JsonResponse({'error': 'Book not found'}, status=404)

# Tag views (showing reverse relations)
def tag_list(request):
    tags = Tag.objects.all()
    data = serialize_queryset_to_list(tags, include_relations=[
        'comments',
        'comments.book',
        'comments.book.author'
    ])
    return JsonResponse(data, safe=False)

def tag_detail(request, pk):
    try:
        tag = Tag.objects.get(pk=pk)
        data = serialize_instance_to_dict(tag, include_relations=[
            'comments',
            'comments.book',
            'comments.book.author',
            'comments.book.author.publisher'
        ])
        return JsonResponse(data)
    except Tag.DoesNotExist:
        return JsonResponse({'error': 'Tag not found'}, status=404)