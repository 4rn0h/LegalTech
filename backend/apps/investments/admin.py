from django.contrib import admin

from .models import Investment, InvestmentBenchmark, Portfolio


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    list_display = [
        "client",
        "total_value",
        "total_return",
        "total_return_percentage",
        "updated_at",
    ]
    search_fields = ["client__email"]
    readonly_fields = [
        "total_value",
        "total_return",
        "total_return_percentage",
        "created_at",
        "updated_at",
    ]
    ordering = ["-updated_at"]


@admin.register(Investment)
class InvestmentAdmin(admin.ModelAdmin):
    list_display = [
        "portfolio",
        "symbol",
        "name",
        "investment_type",
        "quantity",
        "current_value",
        "gain_loss_percentage",
    ]
    list_filter = ["investment_type", "created_at"]
    search_fields = ["symbol", "name", "portfolio__client__email"]
    readonly_fields = [
        "current_value",
        "gain_loss",
        "gain_loss_percentage",
        "created_at",
        "updated_at",
    ]
    ordering = ["-created_at"]


@admin.register(InvestmentBenchmark)
class InvestmentBenchmarkAdmin(admin.ModelAdmin):
    list_display = [
        "portfolio",
        "benchmark_name",
        "benchmark_return",
        "benchmark_value",
    ]
    search_fields = ["benchmark_name", "portfolio__client__email"]
    readonly_fields = ["created_at", "updated_at"]
