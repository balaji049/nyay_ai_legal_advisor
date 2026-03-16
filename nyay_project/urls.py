# ============================================================
# nyay_project/urls.py — Master URL Router
# ============================================================
# This is the "front door" for all incoming URLs.
# Django reads this file and routes requests to the right view.
#
# In Flask, you put @app.route() on every function.
# In Django, all routes are declared HERE in one central place.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin panel — available at /admin/
    # Login with the superuser account you create via: python manage.py createsuperuser
    path("admin/", admin.site.urls),

    # All our app routes — delegated to chat/urls.py
    # include("chat.urls") means: go look in chat/urls.py for the rest
    path("", include("chat.urls")),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)