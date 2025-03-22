# yourapp/management/commands/seed_data.py

import random
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.posts.models import *
import string

from apps.posts.seed import create_blogs, run_all_seeders

class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Seeding data...'))

        def generate_random_string(length=10):
            """Generate a random string of alphanumeric characters."""
            return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

        create_blogs()
        run_all_seeders()

        self.stdout.write(self.style.SUCCESS('Data seeded successfully!'))
