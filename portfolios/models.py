from django.db import models
from users.models import User
from funds.models import Fund

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio of {self.user.email}"

    def total_invested_amount(self):
        return round(sum(folio.total_invested_amount() for folio in self.folios.all()), 2)

    def total_current_value(self):
        return round(sum(folio.total_current_value() for folio in self.folios.all()), 2)

    def total_performance(self):
        invested_amount = self.total_invested_amount()
        current_value = self.total_current_value()
        return round(((current_value - invested_amount) / invested_amount) * 100, 2) if invested_amount > 0 else 0


class Folio(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='folios', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Folio {self.name} in Portfolio {self.portfolio.id}"

    def total_invested_amount(self):
        return round(sum(fundfolio.total_invested_amount() for fundfolio in self.fundfolios.all()), 2)

    def total_current_value(self):
        return round(sum(fundfolio.current_value() for fundfolio in self.fundfolios.all()), 2)

    def performance(self):
        invested_amount = self.total_invested_amount()
        current_value = self.total_current_value()
        return round(((current_value - invested_amount) / invested_amount) * 100, 2) if invested_amount > 0 else 0


class FundFolio(models.Model):
    folio = models.ForeignKey(Folio, related_name='fundfolios', on_delete=models.CASCADE)
    fund = models.ForeignKey('funds.Fund', related_name='fundfolios', on_delete=models.CASCADE)
    units_held = models.DecimalField(max_digits=10, decimal_places=2)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Fund {self.fund.name} in Folio {self.folio.name}"

    def total_invested_amount(self):
        return round(self.units_held * self.average_cost, 2)

    def current_value(self):
        return round(self.fund.nav * self.units_held, 2)

    def performance(self):
        invested_amount = self.total_invested_amount()
        return round(((self.current_value() - invested_amount) / invested_amount) * 100, 2) if invested_amount > 0 else 0


class Transaction(models.Model):
    TRANSACTION_TYPE_CHOICES = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    portfolio = models.ForeignKey('Portfolio', on_delete=models.CASCADE)  # ForeignKey to Portfolio
    units = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=4, choices=TRANSACTION_TYPE_CHOICES)
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type} - {self.units} units of {self.fund.name}"