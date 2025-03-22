import datetime

from apps.posts.models import *


def create_blogs():
    blogs = [
        {
            "title": "Introduction to Django",
            "content": "Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design."
        },
        {
            "title": "Getting Started with Django Models",
            "content": "Models are the single, definitive source of truth about your data. They contain the essential fields and behaviors of the data you’re storing."
        },
        {
            "title": "Django Views and URLconfs",
            "content": "A view function, or view for short, is a Python function that takes a Web request and returns a Web response."
        },
        {
            "title": "Understanding Django Templates",
            "content": "Templates are used to generate HTML dynamically. A template contains the static parts of the desired HTML output as well as some special syntax describing how dynamic content will be inserted."
        },
        {
            "title": "Django Admin Interface",
            "content": "Django provides a built-in admin interface which makes it easy to perform CRUD (Create, Read, Update, Delete) operations on your models."
        }
    ]

    for blog_data in blogs:
        Blog.objects.create(
            title=blog_data["title"],
            content=blog_data["content"],
        )

    print("Blogs created successfully.")




def create_authors():
    authors = [
        {"name": "J.K. Rowling"},
        {"name": "George R.R. Martin"},
        {"name": "Jane Austen"},
        {"name": "Stephen King"},
        {"name": "Agatha Christie"}
    ]
    
    author_objects = []
    for author_data in authors:
        author = Author.objects.create(
            name=author_data["name"]
        )
        author_objects.append(author)
        
    print("Authors created successfully.")
    return author_objects


def create_books(authors):
    books = [
        {"title": "Harry Potter and the Philosopher's Stone", "author": authors[0]},
        {"title": "Harry Potter and the Chamber of Secrets", "author": authors[0]},
        {"title": "A Game of Thrones", "author": authors[1]},
        {"title": "A Clash of Kings", "author": authors[1]},
        {"title": "Pride and Prejudice", "author": authors[2]},
        {"title": "The Shining", "author": authors[3]},
        {"title": "Murder on the Orient Express", "author": authors[4]}
    ]
    
    book_objects = []
    for book_data in books:
        book = Book.objects.create(
            title=book_data["title"],
            author=book_data["author"]
        )
        book_objects.append(book)
        
    print("Books created successfully.")
    return book_objects


def create_comments(books):
    comments = [
        {"content": "This book changed my life!", "book": books[0]},
        {"content": "A magical masterpiece", "book": books[0]},
        {"content": "Even better than the first one", "book": books[1]},
        {"content": "Winter is coming...", "book": books[2]},
        {"content": "Complex characters and intriguing plot", "book": books[3]},
        {"content": "A timeless classic", "book": books[4]},
        {"content": "Absolutely terrifying!", "book": books[5]},
        {"content": "Best mystery novel ever written", "book": books[6]},
        {"content": "The ending was so unexpected", "book": books[6]}
    ]
    
    comment_objects = []
    for comment_data in comments:
        comment = Comment.objects.create(
            content=comment_data["content"],
            book=comment_data["book"]
        )
        comment_objects.append(comment)
        
    print("Comments created successfully.")
    return comment_objects


# You can run all seeders together like this:
def run_all_seeders():
    authors = create_authors()
    books = create_books(authors)
    comments = create_comments(books)
    print("All data seeded successfully!")