from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Client, ClientDocument, ClientInteraction
from .serializers import (
    ClientDetailSerializer,
    ClientDocumentSerializer,
    ClientInteractionSerializer,
    ClientSerializer,
)


class ClientViewSet(viewsets.ModelViewSet):
    """Client management endpoints"""

    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["first_name", "last_name", "email", "company_name"]
    ordering_fields = ["created_at", "last_name", "first_name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Filter clients by the authenticated user"""
        user = self.request.user
        if user.is_staff:
            return Client.objects.all()
        return Client.objects.filter(professional=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ClientDetailSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        """Set the professional to the current user"""
        serializer.save(professional=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_onboarded(self, request, pk=None):
        """Mark client as onboarded"""
        client = self.get_object()
        client.onboarding_completed = True
        client.save()
        return Response({"detail": "Client marked as onboarded"})

    @action(detail=True, methods=["post"])
    def archive(self, request, pk=None):
        """Archive a client"""
        client = self.get_object()
        client.relationship_status = "archived"
        client.save()
        return Response({"detail": "Client archived"})


class ClientDocumentViewSet(viewsets.ModelViewSet):
    """Client document management"""

    queryset = ClientDocument.objects.all()
    serializer_class = ClientDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]

    def get_queryset(self):
        """Only show documents from the user's clients"""
        user = self.request.user
        if user.is_staff:
            return ClientDocument.objects.all()
        return ClientDocument.objects.filter(client__professional=user)

    def perform_create(self, serializer):
        """Set the uploaded_by to the current user"""
        serializer.save(uploaded_by=self.request.user)

    @action(detail=True, methods=["post"])
    def share(self, request, pk=None):
        """Share document with other users"""
        document = self.get_object()
        user_ids = request.data.get("user_ids", [])

        from apps.users.models import CustomUser

        users = CustomUser.objects.filter(id__in=user_ids)
        document.shared_with.set(users)

        return Response({"detail": f"Document shared with {users.count()} users"})


class ClientInteractionViewSet(viewsets.ModelViewSet):
    """Client interaction logging"""

    queryset = ClientInteraction.objects.all()
    serializer_class = ClientInteractionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["subject", "notes"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Only show interactions from the user's clients"""
        user = self.request.user
        if user.is_staff:
            return ClientInteraction.objects.all()
        return ClientInteraction.objects.filter(client__professional=user)

    def perform_create(self, serializer):
        """Set the interacted_by to the current user"""
        serializer.save(interacted_by=self.request.user)
