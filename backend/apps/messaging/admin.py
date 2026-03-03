from django.contrib import admin

from .models import Conversation, Message


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "is_group", "participant_count", "updated_at"]
    list_filter = ["is_group", "created_at"]
    search_fields = ["name", "participants__email"]
    filter_horizontal = ["participants"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-updated_at"]

    def participant_count(self, obj):
        return obj.participants.count()

    participant_count.short_description = "Participants"


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = [
        "sender",
        "conversation",
        "content_preview",
        "is_edited",
        "created_at",
    ]
    list_filter = ["is_edited", "created_at"]
    search_fields = ["content", "sender__email", "conversation__name"]
    readonly_fields = ["created_at"]
    filter_horizontal = ["read_by"]
    ordering = ["-created_at"]

    def content_preview(self, obj):
        return obj.content[:50] + "..." if len(obj.content) > 50 else obj.content

    content_preview.short_description = "Content"
