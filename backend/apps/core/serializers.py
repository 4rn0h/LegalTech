from rest_framework import serializers

from .models import AuditLog, SystemSetting


class AuditLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuditLog
        fields = [
            "id",
            "user_email",
            "action",
            "model_name",
            "object_id",
            "changes",
            "ip_address",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]


class SystemSettingSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSetting
        fields = ["id", "key", "value", "description", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]
