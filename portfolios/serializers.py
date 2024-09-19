from rest_framework import serializers
from .models import Portfolio, Folio, FundFolio
from funds.serializers import FundSerializer

# Serializer for funds within folios (FundFolio model)
class FundFolioSerializer(serializers.ModelSerializer):
    fund = FundSerializer(read_only=True)  # Nested fund details

    class Meta:
        model = FundFolio
        fields = ['id', 'folio', 'fund', 'units_held', 'average_cost', 'current_value']  # Specific fields for FundFolio

# Folio serializer with associated funds
class FolioSerializer(serializers.ModelSerializer):
    funds = FundFolioSerializer(many=True, read_only=True)  # Show all funds in the folio

    class Meta:
        model = Folio
        fields = ['id', 'name', 'created_at', 'funds']  # Specified fields for folio

# Portfolio serializer with associated folios
class PortfolioSerializer(serializers.ModelSerializer):
    folios = FolioSerializer(many=True, read_only=True)  # Nested folios within portfolio

    class Meta:
        model = Portfolio
        fields = ['id', 'user', 'folios', 'created_at']  # Include the nested folios
