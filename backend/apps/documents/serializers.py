from rest_framework import serializers

from .models import Document, DocumentAccess, DocumentVersion


class DocumentVersionSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(
        source="uploaded_by.get_full_name", read_only=True
    )

    class Meta:
        model = DocumentVersion
        fields = [
            "id",
            "version_number",
            "file",
            "uploaded_by",
            "uploaded_by_name",
            "change_description",
            "created_at",
        ]
        read_only_fields = ["id", "version_number", "created_at"]


class DocumentAccessSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.get_full_name", read_only=True)

    class Meta:
        model = DocumentAccess
        fields = ["id", "user", "user_name", "action", "created_at"]
        read_only_fields = ["id", "created_at"]


class DocumentSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "owner",
            "owner_name",
            "title",
            "description",
            "document_type",
            "file",
            "file_size",
            "is_confidential",
            "shared_with",
            "version",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "file_size",
            "file_hash",
            "version",
            "created_at",
            "updated_at",
        ]


class DocumentDetailSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="owner.get_full_name", read_only=True)
    versions = DocumentVersionSerializer(many=True, read_only=True)
    access_logs = DocumentAccessSerializer(many=True, read_only=True)

    class Meta:
        model = Document
        fields = [
            "id",
            "owner",
            "owner_name",
            "title",
            "description",
            "document_type",
            "file",
            "file_size",
            "is_confidential",
            "shared_with",
            "version",
            "versions",
            "access_logs",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "owner",
            "file_size",
            "file_hash",
            "version",
            "created_at",
            "updated_at",
        ]
