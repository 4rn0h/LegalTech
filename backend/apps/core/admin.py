from django.contrib import admin

from .models import AuditLog, SystemSetting


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["user_email", "action", "model_name", "object_id", "created_at"]
    list_filter = ["action", "model_name", "created_at"]
    search_fields = ["user_email", "model_name", "object_id"]
    readonly_fields = ["created_at"]
    ordering = ["-created_at"]


@admin.register(SystemSetting)
class SystemSettingAdmin(admin.ModelAdmin):
    list_display = ["key", "value", "updated_at"]
    search_fields = ["key", "description"]
    readonly_fields = ["created_at", "updated_at"]
