from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Investment, InvestmentBenchmark, Portfolio
from .serializers import (
    InvestmentBenchmarkSerializer,
    InvestmentSerializer,
    PortfolioDetailSerializer,
    PortfolioSerializer,
)


class PortfolioViewSet(viewsets.ModelViewSet):
    """Portfolio management"""

    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "head", "options"]

    def get_queryset(self):
        """Only show user's own portfolio"""
        user = self.request.user
        if user.is_staff:
            return Portfolio.objects.all()
        return Portfolio.objects.filter(client=user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return PortfolioDetailSerializer
        return PortfolioSerializer

    @action(detail=False, methods=["get"])
    def me(self, request):
        """Get current user's portfolio"""
        try:
            portfolio = request.user.portfolio
            serializer = PortfolioDetailSerializer(
                portfolio, context={"request": request}
            )
            return Response(serializer.data)
        except Portfolio.DoesNotExist:
            return Response(
                {"error": "Portfolio not found"}, status=status.HTTP_404_NOT_FOUND
            )


class InvestmentViewSet(viewsets.ModelViewSet):
    """Investment management"""

    queryset = Investment.objects.all()
    serializer_class = InvestmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["symbol", "name"]
    ordering = ["-created_at"]

    def get_queryset(self):
        """Only show investments from user's portfolio"""
        user = self.request.user
        if user.is_staff:
            return Investment.objects.all()
        return Investment.objects.filter(portfolio__client=user)


class InvestmentBenchmarkViewSet(viewsets.ModelViewSet):
    """Investment benchmark management"""

    queryset = InvestmentBenchmark.objects.all()
    serializer_class = InvestmentBenchmarkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        """Only show benchmarks for user's portfolio"""
        user = self.request.user
        if user.is_staff:
            return InvestmentBenchmark.objects.all()
        return InvestmentBenchmark.objects.filter(portfolio__client=user)
