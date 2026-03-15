# ============================================================
# nyay_project/wsgi.py — WSGI entry point for production deployment
# ============================================================
# WSGI = Web Server Gateway Interface
# This file is used when deploying to production (Gunicorn, Railway, Heroku, etc.)
# During development you use: python manage.py runserver (which ignores this file)

import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "nyay_project.settings")
application = get_wsgi_application()
