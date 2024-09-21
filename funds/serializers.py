from rest_framework import serializers
from .models import Fund, Theme, RiskProfile
from portfolios.models import FundFolio

class ThemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Theme
        fields = ['id', 'name']

class RiskProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskProfile
        fields = ['id', 'name']

class FundFolioSerializer(serializers.ModelSerializer):
    fund_name = serializers.CharField(source='fund.name', read_only=True)  # Include fund name for better representation
    folio_name = serializers.CharField(source='folio.name', read_only=True)  # Access folio name via related field
    class Meta:
        model = FundFolio
        fields = ['id', 'folio', 'fund', 'fund_name', 'folio_name', 'units_held', 'average_cost', 'current_value']

class FundSerializer(serializers.ModelSerializer):
    themes = ThemeSerializer(many=True)
    risk_profile = RiskProfileSerializer(many=False)
    fundfolios = FundFolioSerializer(many=True, read_only=True)  # Show folios related to the fund
    # Nested relationship

    class Meta:
        model = Fund
        fields = ['id', 'name', 'fund_type', 'nav', 'risk_profile', 'expected_returns', 'investment_duration', 'themes', 'fundfolios']
