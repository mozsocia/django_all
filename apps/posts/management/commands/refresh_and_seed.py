# refresh_and_seed.py

import os
from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Clears all migration files, runs makemigrations, migrate, and seeds data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Deleting db.sqlite3..."))
        self.delete_database()
        self.stdout.write(self.style.SUCCESS("Clearing existing migrations..."))
        self.clear_migrations()
        self.stdout.write(self.style.SUCCESS("Making new migrations..."))
        call_command('makemigrations')
        self.stdout.write(self.style.SUCCESS("Applying migrations..."))
        call_command('migrate')
        self.stdout.write(self.style.SUCCESS("Seeding data..."))
        call_command('seed_data')

    def delete_database(self):
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')

    def clear_migrations(self):
        migrations_dirs = [
                'apps/posts/migrations',       
            ]

        for migrations_dir in migrations_dirs:
            for filename in os.listdir(migrations_dir):
                if filename != '__init__.py':
                    file_path = os.path.join(migrations_dir, filename)
                    try:
                        os.remove(file_path)
                    except PermissionError as e:
                        pass
                        # self.stderr.write(f"Permission error: {e}. Skipping {file_path}")
