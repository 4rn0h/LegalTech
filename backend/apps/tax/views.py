from rest_framework import filters, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import TaxDeduction, TaxDocument, TaxReturn
from .serializers import (
    TaxDeductionSerializer,
    TaxDocumentSerializer,
    TaxReturnDetailSerializer,
    TaxReturnSerializer,
)


class TaxReturnViewSet(viewsets.ModelViewSet):
    """Tax return management"""

    queryset = TaxReturn.objects.all()
    serializer_class = TaxReturnSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["tax_year", "created_at"]
    ordering = ["-tax_year"]

    def get_queryset(self):
        """Filter by client ownership"""
        user = self.request.user
        if user.is_staff:
            return TaxReturn.objects.all()
        return TaxReturn.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return TaxReturnDetailSerializer
        return TaxReturnSerializer

    @action(detail=True, methods=["post"])
    def file_return(self, request, pk=None):
        """Mark tax return as filed"""
        tax_return = self.get_object()
        from django.utils import timezone

        tax_return.status = "filed"
        tax_return.filing_date = timezone.now().date()
        tax_return.save()
        return Response({"detail": "Tax return marked as filed"})


class TaxDocumentViewSet(viewsets.ModelViewSet):
    """Tax document management"""

    queryset = TaxDocument.objects.all()
    serializer_class = TaxDocumentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["document_type"]

    def get_queryset(self):
        """Only show documents from user's tax returns"""
        user = self.request.user
        if user.is_staff:
            return TaxDocument.objects.all()
        return TaxDocument.objects.filter(tax_return__client=user)

    def perform_create(self, serializer):
        """Set uploaded_by to current user"""
        serializer.save(uploaded_by=self.request.user)


class TaxDeductionViewSet(viewsets.ModelViewSet):
    """Tax deduction management"""

    queryset = TaxDeduction.objects.all()
    serializer_class = TaxDeductionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["category", "description"]

    def get_queryset(self):
        """Only show deductions from user's tax returns"""
        user = self.request.user
        if user.is_staff:
            return TaxDeduction.objects.all()
        return TaxDeduction.objects.filter(tax_return__client=user)
