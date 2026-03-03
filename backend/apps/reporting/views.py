from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import DashboardWidget, Report
from .serializers import DashboardWidgetSerializer, ReportSerializer


class ReportViewSet(viewsets.ReadOnlyModelViewSet):
    """Report viewing and generation"""

    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["generated_at"]
    ordering = ["-generated_at"]

    def get_queryset(self):
        """Only show reports created by user or for user"""
        user = self.request.user
        if user.is_staff:
            return Report.objects.all()
        return Report.objects.filter(created_by=user)


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    """Dashboard widget management"""

    queryset = DashboardWidget.objects.all()
    serializer_class = DashboardWidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only show widgets for the authenticated user"""
        return DashboardWidget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Set user to current user"""
        serializer.save(user=self.request.user)

    @action(detail=False, methods=["get"])
    def dashboard(self, request):
        """Get user's full dashboard"""
        widgets = self.get_queryset()
        serializer = self.get_serializer(widgets, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def update_position(self, request, pk=None):
        """Update widget position"""
        widget = self.get_object()
        new_position = request.data.get("position")
        if new_position is not None:
            widget.position = new_position
            widget.save()
            return Response({"detail": "Position updated"})
        return Response(
            {"error": "Position not provided"}, status=status.HTTP_400_BAD_REQUEST
        )
