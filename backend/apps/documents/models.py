from django.db import models

from apps.users.models import CustomUser


class Document(models.Model):
    """Encrypted document storage with version control"""

    DOCUMENT_TYPES = [
        ("legal", "Legal Document"),
        ("tax", "Tax Document"),
        ("financial", "Financial Document"),
        ("contract", "Contract"),
        ("agreement", "Agreement"),
        ("report", "Report"),
        ("other", "Other"),
    ]

    owner = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="documents"
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    document_type = models.CharField(
        max_length=20, choices=DOCUMENT_TYPES, default="other"
    )

    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    file_size = models.BigIntegerField(editable=False)
    file_hash = models.CharField(max_length=256, unique=True)

    is_confidential = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(
        CustomUser, related_name="shared_documents", blank=True
    )

    version = models.PositiveIntegerField(default=1)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "documents_document"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} (v{self.version})"


class DocumentVersion(models.Model):
    """Track document versions"""

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="versions"
    )
    version_number = models.PositiveIntegerField()
    file = models.FileField(upload_to="documents/versions/%Y/%m/%d/")
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    change_description = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents_documentversion"
        unique_together = ["document", "version_number"]
        ordering = ["-version_number"]

    def __str__(self):
        return f"{self.document.title} - Version {self.version_number}"


class DocumentAccess(models.Model):
    """Log document access for audit trail"""

    document = models.ForeignKey(
        Document, on_delete=models.CASCADE, related_name="access_logs"
    )
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    action = models.CharField(
        max_length=50,
        choices=[
            ("viewed", "Viewed"),
            ("downloaded", "Downloaded"),
            ("shared", "Shared"),
        ],
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "documents_documentaccess"
        ordering = ["-created_at"]
