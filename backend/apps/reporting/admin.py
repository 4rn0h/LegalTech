from django.contrib import admin

from .models import DashboardWidget, Report


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ["title", "report_type", "created_by", "generated_at"]
    list_filter = ["report_type", "generated_at"]
    search_fields = ["title", "description", "created_by__email"]
    readonly_fields = ["generated_at"]
    ordering = ["-generated_at"]


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ["user", "title", "widget_type", "position", "updated_at"]
    list_filter = ["widget_type", "created_at"]
    search_fields = ["user__email", "title"]
    readonly_fields = ["created_at", "updated_at"]
    ordering = ["user", "position"]
