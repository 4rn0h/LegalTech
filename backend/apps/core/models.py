from django.db import models


class AuditLog(models.Model):
    """Audit log for tracking important actions"""

    ACTION_TYPES = [
        ("create", "Create"),
        ("update", "Update"),
        ("delete", "Delete"),
        ("access", "Access"),
        ("login", "Login"),
        ("logout", "Logout"),
    ]

    user_email = models.EmailField()
    action = models.CharField(max_length=20, choices=ACTION_TYPES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100, blank=True, null=True)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "core_auditlog"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user_email", "-created_at"]),
            models.Index(fields=["model_name"]),
        ]

    def __str__(self):
        return f"{self.user_email} - {self.action} {self.model_name}"


class SystemSetting(models.Model):
    """System-wide settings"""

    key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "core_systemsetting"

    def __str__(self):
        return self.key
