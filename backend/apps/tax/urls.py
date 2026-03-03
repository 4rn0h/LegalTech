from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TaxDeductionViewSet, TaxDocumentViewSet, TaxReturnViewSet

router = DefaultRouter()
router.register(r"returns", TaxReturnViewSet, basename="tax-return")
router.register(r"documents", TaxDocumentViewSet, basename="tax-document")
router.register(r"deductions", TaxDeductionViewSet, basename="tax-deduction")

app_name = "tax"

urlpatterns = [
    path("", include(router.urls)),
]
