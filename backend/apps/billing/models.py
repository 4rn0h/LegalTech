from django.db import models

from apps.users.models import CustomUser


class Invoice(models.Model):
    """Client invoices"""

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("sent", "Sent"),
        ("viewed", "Viewed"),
        ("paid", "Paid"),
        ("overdue", "Overdue"),
        ("cancelled", "Cancelled"),
    ]

    client = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="invoices"
    )
    issued_by = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, related_name="issued_invoices"
    )

    invoice_number = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    amount = models.DecimalField(max_digits=12, decimal_places=2)
    tax_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)

    issue_date = models.DateField()
    due_date = models.DateField()
    paid_date = models.DateField(blank=True, null=True)

    notes = models.TextField(blank=True, null=True)
    stripe_invoice_id = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_invoice"
        ordering = ["-issue_date"]
        unique_together = ["client", "invoice_number"]

    def __str__(self):
        return f"Invoice {self.invoice_number}"


class Payment(models.Model):
    """Payment records"""

    PAYMENT_METHODS = [
        ("credit_card", "Credit Card"),
        ("bank_transfer", "Bank Transfer"),
        ("check", "Check"),
        ("paypal", "PayPal"),
    ]

    invoice = models.ForeignKey(
        Invoice, on_delete=models.CASCADE, related_name="payments"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    transaction_id = models.CharField(max_length=255, blank=True, null=True)
    reference_number = models.CharField(max_length=255, blank=True, null=True)

    paid_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "billing_payment"
        ordering = ["-paid_at"]

    def __str__(self):
        return f"Payment for {self.invoice.invoice_number} - ${self.amount}"


class BillingCycle(models.Model):
    """Billing cycle settings for clients"""

    FREQUENCY_CHOICES = [
        ("monthly", "Monthly"),
        ("quarterly", "Quarterly"),
        ("semi_annual", "Semi-Annual"),
        ("annual", "Annual"),
    ]

    client = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="billing_cycle"
    )
    frequency = models.CharField(
        max_length=20, choices=FREQUENCY_CHOICES, default="monthly"
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    next_billing_date = models.DateField()
    active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "billing_billingcycle"

    def __str__(self):
        return f"Billing Cycle for {self.client.email}"
