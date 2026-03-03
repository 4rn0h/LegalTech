from django.db import models

from apps.users.models import CustomUser


class Client(models.Model):
    """Client profile and information"""

    RELATIONSHIP_CHOICES = [
        ("active", "Active"),
        ("archived", "Archived"),
        ("prospective", "Prospective"),
    ]

    # Related users
    professional = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="managed_clients",
        help_text="Professional/Advisor managing this client",
    )
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="client_profile",
        help_text="Client user account (if applicable)",
    )

    # Personal Info
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    # Address
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    # Professional Info
    company_name = models.CharField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    job_title = models.CharField(max_length=100, blank=True, null=True)

    # Relationship Info
    relationship_status = models.CharField(
        max_length=20, choices=RELATIONSHIP_CHOICES, default="active"
    )
    onboarding_completed = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clients_client"
        ordering = ["-created_at"]
        unique_together = ["professional", "email"]

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class ClientDocument(models.Model):
    """Documents associated with a client"""

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="documents"
    )
    uploaded_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to="client_documents/%Y/%m/%d/")
    category = models.CharField(max_length=100, blank=True, null=True)

    is_sensitive = models.BooleanField(default=False)
    shared_with = models.ManyToManyField(
        CustomUser, related_name="client_shared_documents", blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "clients_clientdocument"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client.full_name} - {self.title}"


class ClientInteraction(models.Model):
    """Log of interactions with a client"""

    INTERACTION_TYPES = [
        ("email", "Email"),
        ("call", "Phone Call"),
        ("meeting", "In-person Meeting"),
        ("video_call", "Video Call"),
        ("message", "In-app Message"),
    ]

    client = models.ForeignKey(
        Client, on_delete=models.CASCADE, related_name="interactions"
    )
    interacted_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)

    interaction_type = models.CharField(max_length=20, choices=INTERACTION_TYPES)
    subject = models.CharField(max_length=255)
    notes = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "clients_clientinteraction"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.client.full_name} - {self.interaction_type} on {self.created_at.date()}"
