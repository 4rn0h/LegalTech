from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import CustomUser, UserProfile


@admin.register(CustomUser)
class CustomUserAdmin(BaseUserAdmin):
    list_display = [
        "email",
        "username",
        "role",
        "is_email_verified",
        "mfa_enabled",
        "created_at",
    ]
    list_filter = ["role", "is_email_verified", "mfa_enabled", "created_at"]
    search_fields = ["email", "username", "first_name", "last_name"]
    ordering = ["-created_at"]

    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Personal Info",
            {"fields": ("first_name", "last_name", "phone_number", "avatar_url")},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Security", {"fields": ("is_email_verified", "mfa_enabled", "last_login_ip")}),
        ("Role", {"fields": ("role",)}),
        (
            "Timestamps",
            {
                "fields": ("last_login", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "username", "password1", "password2"),
            },
        ),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "company_name", "specialization", "timezone", "updated_at"]
    search_fields = ["user__email", "company_name", "specialization"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-updated_at"]
