from django.db import models

from apps.users.models import CustomUser


class Portfolio(models.Model):
    """Investment portfolio for a client"""

    client = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="portfolio"
    )
    total_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    total_return = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_return_percentage = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "investments_portfolio"

    def __str__(self):
        return f"Portfolio for {self.client.email}"


class Investment(models.Model):
    """Individual investment"""

    INVESTMENT_TYPES = [
        ("stock", "Stock"),
        ("bond", "Bond"),
        ("mutual_fund", "Mutual Fund"),
        ("etf", "ETF"),
        ("real_estate", "Real Estate"),
        ("crypto", "Cryptocurrency"),
        ("other", "Other"),
    ]

    portfolio = models.ForeignKey(
        Portfolio, on_delete=models.CASCADE, related_name="investments"
    )
    symbol = models.CharField(max_length=20)  # Ticker symbol
    name = models.CharField(max_length=255)
    investment_type = models.CharField(max_length=20, choices=INVESTMENT_TYPES)

    purchase_price = models.DecimalField(max_digits=15, decimal_places=2)
    quantity = models.DecimalField(max_digits=15, decimal_places=4)
    current_price = models.DecimalField(max_digits=15, decimal_places=2)
    purchase_date = models.DateField()

    current_value = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gain_loss = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    gain_loss_percentage = models.DecimalField(
        max_digits=8, decimal_places=2, default=0
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "investments_investment"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.symbol}) - {self.quantity} units"


class InvestmentBenchmark(models.Model):
    """Benchmark for comparing portfolio performance"""

    portfolio = models.OneToOneField(
        Portfolio, on_delete=models.CASCADE, related_name="benchmark"
    )
    benchmark_name = models.CharField(max_length=100)  # e.g., 'S&P 500'
    benchmark_return = models.DecimalField(max_digits=8, decimal_places=2)
    benchmark_value = models.DecimalField(max_digits=15, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "investments_investmentbenchmark"

    def __str__(self):
        return f"Benchmark {self.benchmark_name} for {self.portfolio.client.email}"
