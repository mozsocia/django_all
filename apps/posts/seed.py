# seeders.py
import random
from datetime import date, timedelta
from django.utils import timezone

from apps.posts.models import *

def create_publishers():
    publishers = [
        {"name": "Bloomsbury", "founded_year": 1986},
        {"name": "Penguin Random House", "founded_year": 2013},
        {"name": "HarperCollins", "founded_year": 1989},
        {"name": "Scholastic", "founded_year": 1920}
    ]
    
    publisher_objects = []
    for pub_data in publishers:
        publisher = Publisher.objects.create(
            name=pub_data["name"],
            founded_year=pub_data["founded_year"]
        )
        publisher_objects.append(publisher)
        
    print("Publishers created successfully.")
    return publisher_objects

def create_authors(publishers):
    authors = [
        {"name": "J.K. Rowling", "publisher": publishers[0], "birth_date": date(1965, 7, 31)},
        {"name": "George R.R. Martin", "publisher": publishers[1], "birth_date": date(1948, 9, 20)},
        {"name": "Jane Austen", "publisher": publishers[2], "birth_date": date(1775, 12, 16)},
        {"name": "Stephen King", "publisher": publishers[1], "birth_date": date(1947, 9, 21)},
        {"name": "Agatha Christie", "publisher": publishers[3], "birth_date": date(1890, 9, 15)}
    ]
    
    author_objects = []
    for author_data in authors:
        author = Author.objects.create(
            name=author_data["name"],
            publisher=author_data["publisher"],
            birth_date=author_data["birth_date"]
        )
        author_objects.append(author)
        
    print("Authors created successfully.")
    return author_objects

def create_books(authors):
    books = [
        {"title": "Harry Potter and the Philosopher's Stone", "author": authors[0], "published_date": date(1997, 6, 26), "isbn": "9780747532743"},
        {"title": "Harry Potter and the Chamber of Secrets", "author": authors[0], "published_date": date(1998, 7, 2), "isbn": "9780747538486"},
        {"title": "A Game of Thrones", "author": authors[1], "published_date": date(1996, 8, 1), "isbn": "9780553103540"},
        {"title": "A Clash of Kings", "author": authors[1], "published_date": date(1998, 11, 16), "isbn": "9780553108033"},
        {"title": "Pride and Prejudice", "author": authors[2], "published_date": date(1813, 1, 28), "isbn": ""},
        {"title": "The Shining", "author": authors[3], "published_date": date(1977, 1, 28), "isbn": "9780385121675"},
        {"title": "Murder on the Orient Express", "author": authors[4], "published_date": date(1934, 1, 1), "isbn": ""}
    ]
    
    book_objects = []
    for book_data in books:
        book = Book.objects.create(
            title=book_data["title"],
            author=book_data["author"],
            published_date=book_data["published_date"],
            isbn=book_data["isbn"]
        )
        book_objects.append(book)
        
    print("Books created successfully.")
    return book_objects

def create_chapters(books):
    chapter_objects = []
    
    for book in books:
        # Create 5-10 chapters for each book
        num_chapters = random.randint(5, 10)
        for i in range(1, num_chapters + 1):
            chapter = Chapter.objects.create(
                book=book,
                title=f"Chapter {i}",
                number=i
            )
            chapter_objects.append(chapter)
    
    print("Chapters created successfully.")
    return chapter_objects

def create_comments(books, chapters):
    comments = [
        {"content": "This book changed my life!", "book": books[0], "chapter": chapters[0]},
        {"content": "A magical masterpiece", "book": books[0], "chapter": chapters[1]},
        {"content": "Even better than the first one", "book": books[1], "chapter": None},
        {"content": "Winter is coming...", "book": books[2], "chapter": chapters[10]},
        {"content": "Complex characters and intriguing plot", "book": books[3], "chapter": None},
        {"content": "A timeless classic", "book": books[4], "chapter": chapters[20]},
        {"content": "Absolutely terrifying!", "book": books[5], "chapter": chapters[30]},
        {"content": "Best mystery novel ever written", "book": books[6], "chapter": None},
        {"content": "The ending was so unexpected", "book": books[6], "chapter": chapters[40]}
    ]
    
    comment_objects = []
    for comment_data in comments:
        comment = Comment.objects.create(
            content=comment_data["content"],
            book=comment_data["book"],
            chapter=comment_data["chapter"],
            created_at=timezone.now() - timedelta(days=random.randint(1, 100))
        )
        comment_objects.append(comment)
        
    print("Comments created successfully.")
    return comment_objects

def create_tags(comments):
    tags = ["Inspiring", "Funny", "Insightful", "Critical", "Helpful", "Confusing", "Spoiler"]
    
    tag_objects = []
    for tag_name in tags:
        tag = Tag.objects.create(name=tag_name)
        tag_objects.append(tag)
    
    # Assign random tags to comments
    for comment in comments:
        num_tags = random.randint(1, 3)
        selected_tags = random.sample(tag_objects, num_tags)
        for tag in selected_tags:
            tag.comments.add(comment)
    
    print("Tags created successfully.")
    return tag_objects

def run_all_seeders():
    publishers = create_publishers()
    authors = create_authors(publishers)
    books = create_books(authors)
    chapters = create_chapters(books)
    comments = create_comments(books, chapters)
    tags = create_tags(comments)
    print("All data seeded successfully!")
    return publishers, authors, books, chapters, comments, tags