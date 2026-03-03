from django.db import models

from apps.users.models import CustomUser


class Conversation(models.Model):
    """A conversation between two or more users"""

    participants = models.ManyToManyField(CustomUser, related_name="conversations")
    is_group = models.BooleanField(default=False)
    name = models.CharField(
        max_length=255, blank=True, null=True
    )  # For group conversations

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "messaging_conversation"
        ordering = ["-updated_at"]

    def __str__(self):
        if self.is_group:
            return self.name or f"Group {self.id}"
        return f"Conversation {self.id}"


class Message(models.Model):
    """A single message in a conversation"""

    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    sender = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="sent_messages"
    )
    content = models.TextField()

    attachment = models.FileField(
        upload_to="messages/attachments/%Y/%m/%d/", blank=True, null=True
    )
    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(blank=True, null=True)

    read_by = models.ManyToManyField(
        CustomUser, related_name="read_messages", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "messaging_message"
        ordering = ["created_at"]

    def __str__(self):
        return (
            f"{self.sender.username if self.sender else 'Unknown'}: {self.content[:50]}"
        )
