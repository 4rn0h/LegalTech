from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import BillingCycleViewSet, InvoiceViewSet, PaymentViewSet

router = DefaultRouter()
router.register(r"invoices", InvoiceViewSet, basename="invoice")
router.register(r"payments", PaymentViewSet, basename="payment")
router.register(r"cycles", BillingCycleViewSet, basename="billing-cycle")

app_name = "billing"

urlpatterns = [
    path("", include(router.urls)),
]
