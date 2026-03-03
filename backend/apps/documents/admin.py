from django.contrib import admin

from .models import Document, DocumentAccess, DocumentVersion


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "owner",
        "document_type",
        "version",
        "is_confidential",
        "created_at",
    ]
    list_filter = ["document_type", "is_confidential", "created_at"]
    search_fields = ["title", "description", "owner__email"]
    readonly_fields = ["file_hash", "file_size", "created_at", "updated_at"]
    filter_horizontal = ["shared_with"]
    ordering = ["-created_at"]


@admin.register(DocumentVersion)
class DocumentVersionAdmin(admin.ModelAdmin):
    list_display = ["document", "version_number", "uploaded_by", "created_at"]
    list_filter = ["document", "created_at"]
    search_fields = ["document__title"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(DocumentAccess)
class DocumentAccessAdmin(admin.ModelAdmin):
    list_display = ["document", "user", "action", "created_at"]
    list_filter = ["action", "created_at"]
    search_fields = ["document__title", "user__email"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]
