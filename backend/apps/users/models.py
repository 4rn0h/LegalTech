from django.contrib.auth.models import AbstractUser
from django.core.validators import URLValidator
from django.db import models
from django_otp.plugins.otp_static.models import StaticDevice
from django_otp.plugins.otp_totp.models import TOTPDevice


class CustomUser(AbstractUser):
    """Extended user model with additional fields for authentication and profile"""

    ROLE_CHOICES = [
        ("client", "Client"),
        ("professional", "Professional"),
        ("admin", "Administrator"),
    ]

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="client")
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    avatar_url = models.URLField(blank=True, null=True, validators=[URLValidator()])
    is_email_verified = models.BooleanField(default=False)
    mfa_enabled = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_customuser"
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return f"{self.get_full_name()} ({self.email})"

    def enable_mfa(self):
        """Enable MFA for this user"""
        self.mfa_enabled = True
        self.save()

    def disable_mfa(self):
        """Disable MFA for this user"""
        StaticDevice.objects.filter(user=self).delete()
        TOTPDevice.objects.filter(user=self).delete()
        self.mfa_enabled = False
        self.save()


class UserProfile(models.Model):
    """Extended profile for users with professional/organization info"""

    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.TextField(blank=True, null=True)
    company_name = models.CharField(max_length=255, blank=True, null=True)
    specialization = models.CharField(max_length=255, blank=True, null=True)
    timezone = models.CharField(max_length=50, default="UTC")
    notification_preferences = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users_userprofile"
        verbose_name = "User Profile"
        verbose_name_plural = "User Profiles"

    def __str__(self):
        return f"Profile for {self.user.email}"
