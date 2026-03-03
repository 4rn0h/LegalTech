import hashlib

from django.db.models import Q
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Document, DocumentVersion
from .serializers import (
    DocumentDetailSerializer,
    DocumentSerializer,
    DocumentVersionSerializer,
)


class DocumentViewSet(viewsets.ModelViewSet):
    """Document management with versioning"""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "description"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Show documents owned by user or shared with them"""
        user = self.request.user
        if user.is_staff:
            return Document.objects.all()
        return Document.objects.filter(Q(owner=user) | Q(shared_with=user)).distinct()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return DocumentDetailSerializer
        return DocumentSerializer

    def perform_create(self, serializer):
        """Set the owner to current user and compute file hash"""
        file_obj = self.request.FILES.get("file")
        if file_obj:
            file_hash = hashlib.sha256(file_obj.read()).hexdigest()
            file_obj.seek(0)
            serializer.save(
                owner=self.request.user, file_hash=file_hash, file_size=file_obj.size
            )
        else:
            serializer.save(owner=self.request.user)

    @action(detail=True, methods=["post"])
    def share(self, request, pk=None):
        """Share document with other users"""
        document = self.get_object()
        user_ids = request.data.get("user_ids", [])

        from apps.users.models import CustomUser

        users = CustomUser.objects.filter(id__in=user_ids)
        document.shared_with.set(users)

        return Response({"detail": f"Document shared with {users.count()} users"})

    @action(detail=True, methods=["post"])
    def new_version(self, request, pk=None):
        """Upload a new version of the document"""
        document = self.get_object()
        file_obj = request.FILES.get("file")
        change_description = request.data.get("change_description", "")

        if not file_obj:
            return Response(
                {"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create version record
        new_version_number = document.version + 1
        DocumentVersion.objects.create(
            document=document,
            version_number=new_version_number,
            file=file_obj,
            uploaded_by=request.user,
            change_description=change_description,
        )

        # Update document
        file_hash = hashlib.sha256(file_obj.read()).hexdigest()
        file_obj.seek(0)
        document.file = file_obj
        document.version = new_version_number
        document.file_hash = file_hash
        document.file_size = file_obj.size
        document.save()

        return Response(
            {"detail": "New version created", "version": new_version_number}
        )

    @action(detail=True, methods=["get"])
    def versions(self, request, pk=None):
        """Get document version history"""
        document = self.get_object()
        versions = document.versions.all()
        serializer = DocumentVersionSerializer(versions, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def access_log(self, request, pk=None):
        """Get document access audit trail"""
        document = self.get_object()
        access_logs = document.access_logs.all()[:50]  # Last 50 accesses
        from .serializers import DocumentAccessSerializer

        serializer = DocumentAccessSerializer(access_logs, many=True)
        return Response(serializer.data)
