from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import InvestmentBenchmarkViewSet, InvestmentViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r"portfolios", PortfolioViewSet, basename="portfolio")
router.register(r"investments", InvestmentViewSet, basename="investment")
router.register(r"benchmarks", InvestmentBenchmarkViewSet, basename="benchmark")

app_name = "investments"

urlpatterns = [
    path("", include(router.urls)),
]
