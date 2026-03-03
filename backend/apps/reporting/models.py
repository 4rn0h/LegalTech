from django.db import models

from apps.users.models import CustomUser


class Report(models.Model):
    """Generated reports"""

    REPORT_TYPES = [
        ("portfolio", "Portfolio Summary"),
        ("tax", "Tax Summary"),
        ("billing", "Billing Report"),
        ("activity", "Activity Report"),
        ("performance", "Performance Report"),
    ]

    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    data = models.JSONField(default=dict)  # Store report data as JSON
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "reporting_report"
        ordering = ["-generated_at"]

    def __str__(self):
        return f"{self.title} - {self.get_report_type_display()}"


class DashboardWidget(models.Model):
    """Dashboard widget configurations"""

    WIDGET_TYPES = [
        ("summary", "Summary Card"),
        ("chart", "Chart"),
        ("table", "Data Table"),
        ("metric", "Key Metric"),
    ]

    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="dashboard_widgets"
    )
    widget_type = models.CharField(max_length=50, choices=WIDGET_TYPES)
    title = models.CharField(max_length=255)
    position = models.PositiveIntegerField()  # For ordering widgets

    config = models.JSONField(default=dict)  # Widget-specific configuration
    data = models.JSONField(default=dict)  # Cached widget data

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reporting_dashboardwidget"
        ordering = ["position"]
        unique_together = ["user", "position"]

    def __str__(self):
        return f"{self.user.email} - {self.title}"
