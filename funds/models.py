from django.db import models
# FundType Model
class FundType(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# RiskProfile Model
class RiskProfile(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Theme Model
class Theme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

# Fund Model
class Fund(models.Model):
    name = models.CharField(max_length=255)
    fund_type = models.ForeignKey(FundType, on_delete=models.CASCADE)
    nav = models.DecimalField(max_digits=10, decimal_places=2)  # Net Asset Value
    risk_profile = models.ForeignKey(RiskProfile, on_delete=models.CASCADE)
    expected_returns = models.CharField(max_length=50)
    investment_duration = models.CharField(max_length=50)
    themes = models.ManyToManyField(Theme)  # Allowing multiple themes
    created_at = models.DateTimeField(auto_now_add=True)
    folios = models.ManyToManyField('portfolios.Folio', related_name='funds', through='portfolios.FundFolio')

    class Meta:
        indexes = [
            models.Index(fields=['id'])
        ]
    def __str__(self):
        return self.name
