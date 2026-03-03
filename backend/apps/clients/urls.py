from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ClientDocumentViewSet, ClientInteractionViewSet, ClientViewSet

router = DefaultRouter()
router.register(r"", ClientViewSet, basename="client")
router.register(r"documents", ClientDocumentViewSet, basename="document")
router.register(r"interactions", ClientInteractionViewSet, basename="interaction")

app_name = "clients"

urlpatterns = [
    path("", include(router.urls)),
]
