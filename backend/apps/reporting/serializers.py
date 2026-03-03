from rest_framework import serializers

from .models import DashboardWidget, Report


class ReportSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(
        source="created_by.get_full_name", read_only=True
    )

    class Meta:
        model = Report
        fields = [
            "id",
            "created_by",
            "created_by_name",
            "report_type",
            "title",
            "description",
            "data",
            "generated_at",
        ]
        read_only_fields = ["id", "data", "generated_at"]


class DashboardWidgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DashboardWidget
        fields = [
            "id",
            "user",
            "widget_type",
            "title",
            "position",
            "config",
            "data",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "user", "created_at", "updated_at"]
