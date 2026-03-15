# ============================================================
# nyay_project/settings.py — Django Settings for Nyay
# ============================================================
# This is Django's central configuration file.
# It replaces what Flask scattered across app.py, .env loading, etc.
# Django puts EVERYTHING in one place.

import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env file — same as Flask's load_dotenv()
load_dotenv()

# ─── BASE DIRECTORY ────────────────────────────────────────
# Path(__file__) = this file (settings.py)
# .resolve().parent.parent = the nyay-django/ root folder
BASE_DIR = Path(__file__).resolve().parent.parent


# ─── SECURITY ──────────────────────────────────────────────
# SECRET_KEY encrypts sessions and CSRF tokens — keep it secret!
# In Flask this was app.secret_key
SECRET_KEY = os.environ.get("SECRET_KEY", "nyay-django-secret-change-this-in-production")

# DEBUG = True shows detailed error pages during development
# NEVER set DEBUG = True in production (it leaks code)
DEBUG = True

# In production, set this to your domain: ["nyay.yourdomain.com"]
ALLOWED_HOSTS = ["*"]


# ─── INSTALLED APPS ────────────────────────────────────────
# Django uses "apps" — self-contained modules with models, views, urls
# We have one custom app called "chat" which holds all our logic
INSTALLED_APPS = [
    "django.contrib.admin",        # Admin panel at /admin/
    "django.contrib.auth",         # Django's built-in user system
    "django.contrib.contenttypes", # Required by auth
    "django.contrib.sessions",     # Session framework (like Flask sessions)
    "django.contrib.messages",     # One-time flash messages
    "django.contrib.staticfiles",  # Serves CSS/JS/images
    "chat",                        # Our Nyay app ← THIS IS OURS
]


# ─── MIDDLEWARE ────────────────────────────────────────────
# Middleware = functions that run on every request/response
# Order matters! SecurityMiddleware should be first.
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",   # Enables sessions
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",              # CSRF protection (auto!)
    "django.contrib.auth.middleware.AuthenticationMiddleware", # Attaches request.user
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# ─── URL CONFIGURATION ────────────────────────────────────
# The master URL file — tells Django which urls.py to start with
ROOT_URLCONF = "nyay_project.urls"


# ─── TEMPLATES ────────────────────────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],          # Django also checks each app's templates/ folder
        "APP_DIRS": True,    # ← This makes Django find chat/templates/chat/*.html
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Gives templates access to request
                "django.contrib.auth.context_processors.auth", # Gives templates {{ user }}
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "nyay_project.wsgi.application"


# ─── DATABASE ─────────────────────────────────────────────
# Django uses its ORM (Object Relational Mapper) instead of raw SQL
# We define Python classes (models) and Django creates the SQL tables
# SQLite = same as Flask version, stored in db.sqlite3 file
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",  # File saved in the project root
    }
}


# ─── DJANGO AUTH SETTINGS ─────────────────────────────────
# Django has a built-in User model! No need to build users table from scratch.
# These settings control password requirements.
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 6}},
]

# After login, redirect here
LOGIN_REDIRECT_URL = "/"

# If @login_required fails, redirect here
LOGIN_URL = "/login/"

# After logout, redirect here
LOGOUT_REDIRECT_URL = "/login/"


# ─── SESSION SETTINGS ─────────────────────────────────────
# Django sessions are stored in the database (sessions table)
# This is more robust than Flask's cookie-based sessions
SESSION_COOKIE_AGE = 60 * 60 * 24 * 30    # 30 days in seconds
SESSION_SAVE_EVERY_REQUEST = True           # Refresh expiry on each request


# ─── INTERNATIONALIZATION ─────────────────────────────────
LANGUAGE_CODE = "en-us"
TIME_ZONE     = "Asia/Kolkata"   # IST — Indian Standard Time
USE_I18N      = True
USE_TZ        = True


# ─── STATIC FILES ─────────────────────────────────────────
# Static files = CSS, JS, images
STATIC_URL = "/static/"


# ─── DEFAULT PRIMARY KEY ──────────────────────────────────
# Django uses BigAutoField (64-bit integer) as default PK for new models
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# ─── GROQ API (Custom Settings) ────────────────────────────
# Our own settings — not Django built-ins
GROQ_API_KEY  = os.environ.get("GROQ_API_KEY", "")
GROQ_MODELS   = [
    "llama-3.3-70b-versatile",
    "llama-3.1-8b-instant",
    "gemma2-9b-it",
]
