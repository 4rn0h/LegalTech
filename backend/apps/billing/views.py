from django.db.models import Q
from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BillingCycle, Invoice, Payment
from .serializers import BillingCycleSerializer, InvoiceSerializer, PaymentSerializer


class InvoiceViewSet(viewsets.ModelViewSet):
    """Invoice management"""

    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["issue_date", "due_date", "created_at"]
    ordering = ["-issue_date"]

    def get_queryset(self):
        """Show invoices for user's clients or invoices for user"""
        user = self.request.user
        if user.is_staff:
            return Invoice.objects.all()
        return Invoice.objects.filter(Q(issued_by=user) | Q(client=user)).distinct()

    def perform_create(self, serializer):
        """Set issued_by to current user"""
        serializer.save(issued_by=self.request.user)

    @action(detail=True, methods=["post"])
    def mark_as_paid(self, request, pk=None):
        """Mark invoice as paid"""
        invoice = self.get_object()
        from django.utils import timezone

        invoice.status = "paid"
        invoice.paid_date = timezone.now().date()
        invoice.save()
        return Response({"detail": "Invoice marked as paid"})

    @action(detail=True, methods=["post"])
    def send_invoice(self, request, pk=None):
        """Mark invoice as sent"""
        invoice = self.get_object()
        invoice.status = "sent"
        invoice.save()
        # TODO: Implement email notification
        return Response({"detail": "Invoice marked as sent"})


class PaymentViewSet(viewsets.ModelViewSet):
    """Payment recording"""

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = []
    ordering = ["-paid_at"]

    def get_queryset(self):
        """Only show payments for user's invoices"""
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(
            Q(invoice__issued_by=user) | Q(invoice__client=user)
        ).distinct()


class BillingCycleViewSet(viewsets.ModelViewSet):
    """Billing cycle management"""

    queryset = BillingCycle.objects.all()
    serializer_class = BillingCycleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only show billing cycle for user"""
        user = self.request.user
        if user.is_staff:
            return BillingCycle.objects.all()
        return BillingCycle.objects.filter(client=user)
