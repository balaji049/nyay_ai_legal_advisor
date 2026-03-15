#!/usr/bin/env python
"""
Django's command-line utility for administrative tasks.

Usage:
    python manage.py runserver        ← Start the dev server
    python manage.py makemigrations   ← Create migration files from models.py
    python manage.py migrate          ← Apply migrations (creates DB tables)
    python manage.py createsuperuser  ← Create an admin account
"""
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nyay_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and your "
            "virtual environment is activated."
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
