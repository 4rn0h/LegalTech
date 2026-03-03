from rest_framework import serializers

from .models import BillingCycle, Invoice, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "invoice",
            "amount",
            "payment_method",
            "transaction_id",
            "reference_number",
            "paid_at",
        ]
        read_only_fields = ["id", "paid_at"]


class InvoiceSerializer(serializers.ModelSerializer):
    issued_by_name = serializers.CharField(
        source="issued_by.get_full_name", read_only=True
    )
    client_email = serializers.CharField(source="client.email", read_only=True)
    payments = PaymentSerializer(many=True, read_only=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "client",
            "client_email",
            "issued_by",
            "issued_by_name",
            "invoice_number",
            "description",
            "status",
            "amount",
            "tax_amount",
            "total_amount",
            "issue_date",
            "due_date",
            "paid_date",
            "notes",
            "stripe_invoice_id",
            "payments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "issued_by", "payments", "created_at", "updated_at"]


class BillingCycleSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source="client.email", read_only=True)

    class Meta:
        model = BillingCycle
        fields = [
            "id",
            "client",
            "client_email",
            "frequency",
            "amount",
            "next_billing_date",
            "active",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "client_email", "created_at", "updated_at"]
