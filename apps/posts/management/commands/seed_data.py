# yourapp/management/commands/seed_data.py

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.posts.models import *
import string

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        def generate_random_string(length=10):
            """Generate a random string of alphanumeric characters."""
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        def seed_data(num_blogs=3, num_books_per_blog=3):
            for _ in range(num_blogs):
                # Create a new blog
                blog = Blog.objects.create(
                    blog_title=generate_random_string(),
                    blog_details=generate_random_string(50),
                    blog_email=generate_random_string() + '@example.com'
                )

                # Create books for the blog
                for _ in range(num_books_per_blog):
                    Book.objects.create(
                        blog=blog,
                        book_title=generate_random_string(),
                        book_author=generate_random_string()
                    )

        seed_data()

        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))
