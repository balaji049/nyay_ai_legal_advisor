# ============================================================
# chat/admin.py — Register models in Django Admin Panel
# ============================================================
# Django gives you a free admin UI at /admin/
# Register your models here to manage them via the web interface.
# Login with: python manage.py createsuperuser

from django.contrib import admin
from .models import Conversation, Message


class MessageInline(admin.TabularInline):
    """Shows messages nested inside the conversation detail page."""
    model   = Message
    extra   = 0
    readonly_fields = ("role", "content", "created_at")


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display  = ("title", "user", "message_count", "created_at", "updated_at")
    list_filter   = ("user",)
    search_fields = ("title", "user__email")
    inlines       = [MessageInline]

    def message_count(self, obj):
        return obj.messages.count()
    message_count.short_description = "Messages"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ("conversation", "role", "content_preview", "created_at")
    list_filter   = ("role",)
    search_fields = ("content", "conversation__title")

    def content_preview(self, obj):
        return obj.content[:80] + "..." if len(obj.content) > 80 else obj.content
    content_preview.short_description = "Content"
