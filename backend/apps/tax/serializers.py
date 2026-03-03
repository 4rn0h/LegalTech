from rest_framework import serializers

from .models import TaxDeduction, TaxDocument, TaxReturn


class TaxDeductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaxDeduction
        fields = ["id", "category", "amount", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaxDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(
        source="uploaded_by.get_full_name", read_only=True
    )

    class Meta:
        model = TaxDocument
        fields = [
            "id",
            "tax_return",
            "document_type",
            "file",
            "uploaded_by",
            "uploaded_by_name",
            "created_at",
        ]
        read_only_fields = ["id", "uploaded_by", "created_at"]


class TaxReturnSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source="client.email", read_only=True)

    class Meta:
        model = TaxReturn
        fields = [
            "id",
            "client",
            "client_email",
            "tax_year",
            "filing_status",
            "status",
            "gross_income",
            "deductions",
            "taxable_income",
            "total_tax",
            "refund_amount",
            "filing_date",
            "acceptance_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class TaxReturnDetailSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source="client.email", read_only=True)
    documents = TaxDocumentSerializer(many=True, read_only=True)
    deductions = TaxDeductionSerializer(many=True, read_only=True)

    class Meta:
        model = TaxReturn
        fields = [
            "id",
            "client",
            "client_email",
            "tax_year",
            "filing_status",
            "status",
            "gross_income",
            "deductions",
            "taxable_income",
            "total_tax",
            "refund_amount",
            "filing_date",
            "acceptance_date",
            "documents",
            "deductions",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]
