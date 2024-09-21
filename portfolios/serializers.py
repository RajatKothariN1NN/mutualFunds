from rest_framework import serializers
from .models import Portfolio, Folio, FundFolio, Transaction
from funds.serializers import FundSerializer

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'fund', 'portfolio', 'units', 'transaction_type', 'price_per_unit', 'transaction_date']

class FundFolioSerializer(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)  # Nested fund details
    performance = serializers.SerializerMethodField()
    current_value = serializers.SerializerMethodField()
    nav = serializers.DecimalField(max_digits=10, decimal_places=2, source='fund.nav', read_only=True)  # Add NAV field

    class Meta:
        model = FundFolio
        fields = ['id', 'folio', 'fund', 'units_held', 'average_cost', 'current_value', 'performance', 'nav']  # Specific fields for FundFolio

    def get_current_value(self, obj):
        return obj.current_value()

    def get_performance(self, obj):
        return obj.performance()

# Folio serializer with associated funds
class FolioSerializer(serializers.ModelSerializer):
    fundfolios = FundFolioSerializer(many=True, read_only=True)  # Show all funds in the folio
    total_invested_amount = serializers.SerializerMethodField()
    total_current_value = serializers.SerializerMethodField()
    performance = serializers.SerializerMethodField()

    class Meta:
        model = Folio
        fields = ['id', 'name', 'created_at', 'fundfolios', 'total_invested_amount', 'total_current_value', 'performance'] # Specified fields for folio

    def get_total_invested_amount(self, obj):
        return obj.total_invested_amount()

    def get_total_current_value(self, obj):
        return obj.total_current_value()

    def get_performance(self, obj):
        return obj.performance()

# Portfolio serializer with associated folios
class PortfolioSerializer(serializers.ModelSerializer):
    folios = FolioSerializer(many=True, read_only=True)  # Nested folios within portfolio
    total_invested_amount = serializers.SerializerMethodField()
    total_current_value = serializers.SerializerMethodField()
    performance = serializers.SerializerMethodField()
    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'folios', 'created_at', 'total_invested_amount', 'total_current_value', 'performance']  # Include the nested folios

    def get_total_invested_amount(self, obj):
        return obj.total_invested_amount()

    def get_total_current_value(self, obj):
        return obj.total_current_value()

    def get_performance(self, obj):
        return obj.total_performance()


# serializers.py

class BuySellFundSerializer(serializers.Serializer):
    transaction_type = serializers.ChoiceField(choices=['buy', 'sell'])
    fund_id = serializers.IntegerField()
    units = serializers.DecimalField(max_digits=10, decimal_places=2)
    price_per_unit = serializers.DecimalField(max_digits=10, decimal_places=2)
    folio_id = serializers.IntegerField()
