from django.db import models
from users.models import User
from funds.models import Fund

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio of {self.user.email}"

    def total_invested_amount(self):
        return sum(folio.total_invested_amount() for folio in self.folios.all())

    def total_current_value(self):
        return sum(folio.total_current_value() for folio in self.folios.all())

    def total_performance(self):
        invested_amount = self.total_invested_amount()
        current_value = self.total_current_value()
        return ((current_value - invested_amount) / invested_amount) * 100 if invested_amount > 0 else 0


class Folio(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='folios', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Folio {self.name} in Portfolio {self.portfolio.id}"

    def total_invested_amount(self):
        return sum(fundfolio.total_invested_amount() for fundfolio in self.fundfolios.all())

    def total_current_value(self):
        return sum(fundfolio.current_value() for fundfolio in self.fundfolios.all())

    def performance(self):
        invested_amount = self.total_invested_amount()
        current_value = self.total_current_value()
        return ((current_value - invested_amount) / invested_amount) * 100 if invested_amount > 0 else 0


class FundFolio(models.Model):
    folio = models.ForeignKey(Folio, related_name='fundfolios', on_delete=models.CASCADE)
    fund = models.ForeignKey('funds.Fund', related_name='fundfolios', on_delete=models.CASCADE)
    units_held = models.DecimalField(max_digits=10, decimal_places=2)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Fund {self.fund.name} in Folio {self.folio.name}"

    def total_invested_amount(self):
        return self.units_held * self.average_cost

    def current_value(self):
        return self.fund.nav * self.units_held

    def performance(self):
        invested_amount = self.total_invested_amount()
        return ((self.current_value() - invested_amount) / invested_amount) * 100 if invested_amount > 0 else 0