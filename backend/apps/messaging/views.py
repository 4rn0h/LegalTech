from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Conversation, Message
from .serializers import (
    ConversationDetailSerializer,
    ConversationSerializer,
    MessageSerializer,
)


class ConversationViewSet(viewsets.ModelViewSet):
    """Conversation management"""

    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["name"]
    ordering = ["-updated_at"]

    def get_queryset(self):
        """Only show conversations the user is part of"""
        return Conversation.objects.filter(participants=self.request.user).distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ConversationDetailSerializer
        return ConversationSerializer

    def perform_create(self, serializer):
        """Create and add current user to conversation"""
        conversation = serializer.save()
        conversation.participants.add(self.request.user)

    @action(detail=True, methods=["post"])
    def add_participant(self, request, pk=None):
        """Add a participant to the conversation"""
        conversation = self.get_object()
        user_id = request.data.get("user_id")

        from apps.users.models import CustomUser

        try:
            user = CustomUser.objects.get(id=user_id)
            conversation.participants.add(user)
            return Response({"detail": f"{user.get_full_name()} added to conversation"})
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["post"])
    def remove_participant(self, request, pk=None):
        """Remove a participant from the conversation"""
        conversation = self.get_object()
        user_id = request.data.get("user_id")

        from apps.users.models import CustomUser

        try:
            user = CustomUser.objects.get(id=user_id)
            conversation.participants.remove(user)
            return Response(
                {"detail": f"{user.get_full_name()} removed from conversation"}
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )


class MessageViewSet(viewsets.ModelViewSet):
    """Message creation and management"""

    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Only show messages from conversations the user is part of"""
        return Message.objects.filter(conversation__participants=self.request.user)

    def perform_create(self, serializer):
        """Set sender to current user"""
        serializer.save(sender=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_as_read(self, request, pk=None):
        """Mark a message as read"""
        message = self.get_object()
        message.read_by.add(request.user)
        return Response({"detail": "Message marked as read"})

    @action(detail=True, methods=["post"])
    def edit(self, request, pk=None):
        """Edit a message (only by sender)"""
        message = self.get_object()
        if message.sender != request.user:
            return Response(
                {"error": "Only the sender can edit the message"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = self.get_serializer(message, data=request.data, partial=True)
        if serializer.is_valid():
            from django.utils import timezone

            message.content = serializer.validated_data.get("content", message.content)
            message.is_edited = True
            message.edited_at = timezone.now()
            message.save()
            return Response(MessageSerializer(message).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
