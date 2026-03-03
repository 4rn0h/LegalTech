from django.db import models

from apps.users.models import CustomUser


class TaxReturn(models.Model):
    """Tax return records"""

    FILING_STATUS_CHOICES = [
        ("single", "Single"),
        ("married_filing_jointly", "Married Filing Jointly"),
        ("married_filing_separately", "Married Filing Separately"),
        ("head_of_household", "Head of Household"),
        ("qualifying_widow", "Qualifying Widow(er)"),
    ]

    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("filed", "Filed"),
        ("accepted", "Accepted"),
        ("audit", "Under Audit"),
    ]

    client = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="tax_returns"
    )
    tax_year = models.IntegerField()
    filing_status = models.CharField(max_length=30, choices=FILING_STATUS_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    gross_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    taxable_income = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_tax = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    refund_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    filing_date = models.DateField(blank=True, null=True)
    acceptance_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "tax_taxreturn"
        ordering = ["-tax_year", "-created_at"]
        unique_together = ["client", "tax_year"]

    def __str__(self):
        return f"{self.client.email} - Tax Year {self.tax_year}"


class TaxDocument(models.Model):
    """Supporting tax documents"""

    tax_return = models.ForeignKey(
        TaxReturn, on_delete=models.CASCADE, related_name="documents"
    )
    document_type = models.CharField(max_length=100)  # e.g., 'W2', '1099', 'Schedule C'
    file = models.FileField(upload_to="tax_documents/%Y/%m/%d/")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tax_taxdocument"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tax_return} - {self.document_type}"


class TaxDeduction(models.Model):
    """Track tax deductions"""

    tax_return = models.ForeignKey(
        TaxReturn, on_delete=models.CASCADE, related_name="deduction_items"
    )
    category = models.CharField(max_length=100)  # e.g., 'Mortgage Interest', 'Charity'
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "tax_taxdeduction"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.tax_return} - {self.category}: ${self.amount}"
