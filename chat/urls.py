# ============================================================
# chat/urls.py — App-level URL Patterns
# ============================================================
# This file maps URLs to view functions.
# The master urls.py (nyay_project/urls.py) delegates to here.
#
# Flask equivalent: @app.route("/some/path")
# Django equivalent: path("some/path", views.some_function, name="some_name")
#
# The name= parameter lets you use reverse URL lookup in templates:
#   {% url 'index' %}  ← instead of hardcoding "/"

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # ── PAGE ROUTES ──────────────────────────────────────────
    # Home / main chat page
    path("",                    views.index,            name="index"),

    # Open a specific conversation directly
    path("c/<int:conv_id>/",    views.load_conversation, name="load_conversation"),

    # Auth pages
    path("login/",              views.login_view,        name="login"),
    path("signup/",             views.signup_view,       name="signup"),
    path("document-analyzer/", views.document_analyzer, name="document_analyzer"),
    path("legal-generator/", views.generate_legal_document, name="legal_generator"),
    path("sections/", views.law_sections, name="law_sections"),
    path("cases/", views.my_cases, name="my_cases"),
    path("download-pdf/", views.download_pdf, name="download_pdf"),
    path("cases/<int:case_id>/", views.case_detail, name="case_detail"),
    path("profile/", views.profile_page, name="profile"),
    path("doc-chat/upload/", views.upload_doc_chat, name="upload_doc_chat"),
    path(
    "upload-document-context/",
    views.upload_document_context,
    name="upload_document_context"
),
path("doc-chat/", views.doc_chat, name="doc_chat"),
    path("cases/<int:case_id>/edit/", views.edit_case, name="edit_case"),
    path(
    "conversations/<int:conv_id>/pdf/",
    views.export_chat_pdf,
    name="export_chat_pdf"
),
    path("cases/<int:case_id>/pdf/", views.export_case_pdf, name="export_case_pdf"),
path("cases/<int:case_id>/delete/", views.delete_case, name="delete_case"),
path("cases/new/", views.create_case, name="create_case"),

    

    # Django's built-in LogoutView — handles GET /logout/ and clears session
    path("logout/",
         LogoutView.as_view(next_page="/login/"),
         name="logout"),

    # ── API ROUTES ────────────────────────────────────────────
    # These return JSON, not HTML pages
    # Called by JavaScript in index.html via fetch()

    path("api/conversations/",
         views.api_conversations,
         name="api_conversations"),

    path("api/conversations/<int:conv_id>/",
         views.api_conversation_detail,
         name="api_conversation_detail"),

    path("api/chat/",
         views.api_chat,
         name="api_chat"),
]
