from rest_framework import serializers

from .models import Investment, InvestmentBenchmark, Portfolio


class InvestmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Investment
        fields = [
            "id",
            "portfolio",
            "symbol",
            "name",
            "investment_type",
            "purchase_price",
            "quantity",
            "current_price",
            "purchase_date",
            "current_value",
            "gain_loss",
            "gain_loss_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "current_value",
            "gain_loss",
            "gain_loss_percentage",
            "created_at",
            "updated_at",
        ]


class InvestmentBenchmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvestmentBenchmark
        fields = [
            "id",
            "portfolio",
            "benchmark_name",
            "benchmark_return",
            "benchmark_value",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at"]


class PortfolioSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source="client.email", read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "client",
            "client_email",
            "total_value",
            "total_return",
            "total_return_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "client_email",
            "total_value",
            "total_return",
            "total_return_percentage",
            "created_at",
            "updated_at",
        ]


class PortfolioDetailSerializer(serializers.ModelSerializer):
    client_email = serializers.CharField(source="client.email", read_only=True)
    investments = InvestmentSerializer(many=True, read_only=True)
    benchmark = InvestmentBenchmarkSerializer(read_only=True)

    class Meta:
        model = Portfolio
        fields = [
            "id",
            "client",
            "client_email",
            "investments",
            "benchmark",
            "total_value",
            "total_return",
            "total_return_percentage",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "client_email",
            "total_value",
            "total_return",
            "total_return_percentage",
            "created_at",
            "updated_at",
        ]
