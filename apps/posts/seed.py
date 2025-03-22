import datetime

from apps.posts.models import Blog


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