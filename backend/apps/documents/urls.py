from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import DocumentViewSet

router = DefaultRouter()
router.register(r"", DocumentViewSet, basename="document")

app_name = "documents"

urlpatterns = [
    path("", include(router.urls)),
]
