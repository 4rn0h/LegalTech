from django.contrib import admin

from .models import Client, ClientDocument, ClientInteraction


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = [
        "full_name",
        "email",
        "professional",
        "relationship_status",
        "onboarding_completed",
        "created_at",
    ]
    list_filter = ["relationship_status", "onboarding_completed", "created_at"]
    search_fields = ["first_name", "last_name", "email", "company_name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]

    fieldsets = (
        (
            "Personal Information",
            {"fields": ("first_name", "last_name", "email", "phone_number")},
        ),
        (
            "Address",
            {
                "fields": ("address", "city", "state", "postal_code", "country"),
                "classes": ("collapse",),
            },
        ),
        (
            "Professional Information",
            {
                "fields": (
                    "professional",
                    "user",
                    "company_name",
                    "industry",
                    "job_title",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Relationship",
            {"fields": ("relationship_status", "onboarding_completed", "notes")},
        ),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


@admin.register(ClientDocument)
class ClientDocumentAdmin(admin.ModelAdmin):
    list_display = ["title", "client", "category", "is_sensitive", "created_at"]
    list_filter = ["category", "is_sensitive", "created_at"]
    search_fields = ["title", "description", "client__first_name", "client__last_name"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["-created_at"]


@admin.register(ClientInteraction)
class ClientInteractionAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "interaction_type",
        "subject",
        "interacted_by",
        "created_at",
    ]
    list_filter = ["interaction_type", "created_at"]
    search_fields = ["subject", "notes", "client__first_name", "client__last_name"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
