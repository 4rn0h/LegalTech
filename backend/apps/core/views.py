from rest_framework import filters, permissions, viewsets

from .models import AuditLog, SystemSetting
from .serializers import AuditLogSerializer, SystemSettingSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Audit log viewing (admin only)"""

    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["action", "model_name", "user_email"]
    search_fields = ["user_email", "model_name", "object_id"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]


class SystemSettingViewSet(viewsets.ModelViewSet):
    """System settings management (admin only)"""

    queryset = SystemSetting.objects.all()
    serializer_class = SystemSettingSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends = [filters.SearchFilter]
    search_fields = ["key", "description"]
