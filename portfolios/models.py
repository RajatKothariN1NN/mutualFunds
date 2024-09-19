from django.db import models
from users.models import User
from funds.models import Fund

class Portfolio(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Portfolio of {self.user.email}"

class Folio(models.Model):
    portfolio = models.ForeignKey(Portfolio, related_name='folios', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Folio {self.name} in Portfolio {self.portfolio.id}"

class FundFolio(models.Model):
    folio = models.ForeignKey(Folio, related_name='fundfolios', on_delete=models.CASCADE)
    fund = models.ForeignKey('funds.Fund', related_name='fundfolios', on_delete=models.CASCADE)
    units_held = models.DecimalField(max_digits=10, decimal_places=2)
    average_cost = models.DecimalField(max_digits=10, decimal_places=2)
    current_value = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Fund {self.fund.name} in Folio {self.folio.name}"
