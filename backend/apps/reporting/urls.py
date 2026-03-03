from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DashboardWidgetViewSet, ReportViewSet

router = DefaultRouter()
router.register(r"reports", ReportViewSet, basename="report")
router.register(r"widgets", DashboardWidgetViewSet, basename="widget")

app_name = "reporting"

urlpatterns = [
    path("", include(router.urls)),
]
