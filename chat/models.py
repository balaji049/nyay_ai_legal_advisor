# ============================================================
# chat/models.py — Database Models (replaces database.py from Flask)
# ============================================================
# In Flask we wrote raw SQL in database.py.
# In Django we define Python CLASSES here — Django writes the SQL for us!
#
# Each class = one database table.
# Each class attribute = one column.
#
# To create the tables:
#   python manage.py makemigrations   ← generates migration files
#   python manage.py migrate          ← runs the SQL to create tables
#
# IMPORTANT: Django has a built-in User model!
# We do NOT need to create a users table — Django handles it completely.
# It includes: id, username, email, password (hashed), date_joined, etc.
# Located at: django.contrib.auth.models.User

from django.db import models
from django.contrib.auth.models import User  # Built-in Django User!


class Conversation(models.Model):
    """
    One row = one conversation session.

    ForeignKey(User) links each conversation to the user who owns it.
    on_delete=CASCADE means: if the user is deleted, delete their conversations too.

    Flask equivalent in database.py:
        CREATE TABLE conversations (
            id         INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            title      TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    user       = models.ForeignKey(User, on_delete=models.CASCADE, related_name="conversations")
    title      = models.CharField(max_length=200, default="New Conversation")
    created_at = models.DateTimeField(auto_now_add=True)  # Set once on creation
    updated_at = models.DateTimeField(auto_now=True)       # Updated on every save()

    class Meta:
        ordering = ["-updated_at"]   # Default sort: newest first

    def __str__(self):
        return f"{self.title} ({self.user.username})"

    def message_count(self):
        """Helper to count messages — used in the API response."""
        return self.messages.count()


class Message(models.Model):
    """
    One row = one message (either user or assistant).

    ForeignKey(Conversation) links each message to its conversation.
    related_name="messages" allows: conversation.messages.all()

    Flask equivalent in database.py:
        CREATE TABLE messages (
            id              INTEGER PRIMARY KEY AUTOINCREMENT,
            conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
            role            TEXT NOT NULL,    -- 'user' or 'assistant'
            content         TEXT NOT NULL,
            created_at      DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    ROLE_CHOICES = [
        ("user",      "User"),
        ("assistant", "Assistant"),
    ]

    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
    role         = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content      = models.TextField()   # TextField = unlimited text (vs CharField which has max_length)
    created_at   = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]   # Messages always in chronological order

    def __str__(self):
        return f"[{self.role}] {self.content[:50]}"
