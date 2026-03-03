from rest_framework import serializers

from .models import Client, ClientDocument, ClientInteraction


class ClientSerializer(serializers.ModelSerializer):
    professional_name = serializers.CharField(
        source="professional.get_full_name", read_only=True
    )

    class Meta:
        model = Client
        fields = [
            "id",
            "professional",
            "professional_name",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "company_name",
            "industry",
            "job_title",
            "relationship_status",
            "onboarding_completed",
            "notes",
            "full_name",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "full_name"]


class ClientDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(
        source="uploaded_by.get_full_name", read_only=True
    )

    class Meta:
        model = ClientDocument
        fields = [
            "id",
            "client",
            "uploaded_by",
            "uploaded_by_name",
            "title",
            "description",
            "file",
            "category",
            "is_sensitive",
            "shared_with",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "uploaded_by", "created_at", "updated_at"]


class ClientInteractionSerializer(serializers.ModelSerializer):
    interacted_by_name = serializers.CharField(
        source="interacted_by.get_full_name", read_only=True
    )

    class Meta:
        model = ClientInteraction
        fields = [
            "id",
            "client",
            "interacted_by",
            "interacted_by_name",
            "interaction_type",
            "subject",
            "notes",
            "created_at",
        ]
        read_only_fields = ["id", "interacted_by", "created_at"]


class ClientDetailSerializer(serializers.ModelSerializer):
    """Detailed client view with all related data"""

    professional_name = serializers.CharField(
        source="professional.get_full_name", read_only=True
    )
    documents = ClientDocumentSerializer(many=True, read_only=True)
    interactions = ClientInteractionSerializer(many=True, read_only=True)

    class Meta:
        model = Client
        fields = [
            "id",
            "professional",
            "professional_name",
            "user",
            "first_name",
            "last_name",
            "email",
            "phone_number",
            "address",
            "city",
            "state",
            "postal_code",
            "country",
            "company_name",
            "industry",
            "job_title",
            "relationship_status",
            "onboarding_completed",
            "notes",
            "full_name",
            "documents",
            "interactions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at", "full_name"]
