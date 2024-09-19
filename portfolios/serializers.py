from rest_framework import serializers
from .models import Portfolio, Folio, FundFolio
from funds.serializers import FundSerializer

# Serializer for funds within folios (FundFolio model)
class FundFolioSerializer(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)  # Nested fund details
    performance = serializers.SerializerMethodField()
    current_value = serializers.SerializerMethodField()

    class Meta:
        model = FundFolio
        fields = ['id', 'folio', 'fund', 'units_held', 'average_cost', 'current_value', 'performance']  # Specific fields for FundFolio

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