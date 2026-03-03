from django.contrib import admin

from .models import TaxDeduction, TaxDocument, TaxReturn


@admin.register(TaxReturn)
class TaxReturnAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "tax_year",
        "filing_status",
        "status",
        "total_tax",
        "refund_amount",
    ]
    list_filter = ["tax_year", "filing_status", "status", "created_at"]
    search_fields = ["client__email", "client__first_name", "client__last_name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-tax_year", "-created_at"]


@admin.register(TaxDocument)
class TaxDocumentAdmin(admin.ModelAdmin):
    list_display = ["tax_return", "document_type", "uploaded_by", "created_at"]
    list_filter = ["document_type", "created_at"]
    search_fields = ["tax_return__client__email", "document_type"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(TaxDeduction)
class TaxDeductionAdmin(admin.ModelAdmin):
    list_display = ["tax_return", "category", "amount", "created_at"]
    list_filter = ["category", "created_at"]
    search_fields = ["tax_return__client__email", "category"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
