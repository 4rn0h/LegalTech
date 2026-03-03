from django.contrib import admin

from .models import BillingCycle, Invoice, Payment


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = [
        "invoice_number",
        "client",
        "status",
        "total_amount",
        "due_date",
        "paid_date",
    ]
    list_filter = ["status", "issue_date", "due_date"]
    search_fields = ["invoice_number", "client__email", "description"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-issue_date"]


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ["invoice", "amount", "payment_method", "transaction_id", "paid_at"]
    list_filter = ["payment_method", "paid_at"]
    search_fields = ["invoice__invoice_number", "transaction_id"]
    readonly_fields = ["paid_at"]
    ordering = ["-paid_at"]


@admin.register(BillingCycle)
class BillingCycleAdmin(admin.ModelAdmin):
    list_display = ["client", "frequency", "amount", "next_billing_date", "active"]
    list_filter = ["frequency", "active"]
    search_fields = ["client__email"]
    readonly_fields = ["created_at", "updated_at"]
