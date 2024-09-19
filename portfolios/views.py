from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Folio, FundFolio
from .serializers import PortfolioSerializer, FolioSerializer, FundFolioSerializer
from funds.models import Fund


# View for retrieving portfolio details
class PortfolioView(generics.RetrieveAPIView):
    queryset = Portfolio.objects.all()
    serializer_class = PortfolioSerializer
    permission_classes = [IsAuthenticated]


# View for listing all folios of the authenticated user
class FolioView(generics.ListAPIView):
    serializer_class = FolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Folio.objects.filter(portfolio__user=self.request.user)


# View for listing all funds in a user's folios
class FundFolioView(generics.ListAPIView):
    serializer_class = FundFolioSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return FundFolio.objects.filter(folio__portfolio__user=self.request.user)


# New API for creating a new folio
class CreateFolioView(generics.CreateAPIView):
    serializer_class = FolioSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        portfolio = Portfolio.objects.get(user=request.user)
        folio_name = request.data.get('name')

        # Create the folio and associate it with the user's portfolio
        folio = Folio.objects.create(portfolio=portfolio, name=folio_name)
        serializer = self.get_serializer(folio)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# New API for adding a fund to an existing folio
class AddFundToFolioView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, folio_id, *args, **kwargs):
        try:
            folio = Folio.objects.get(id=folio_id, portfolio__user=request.user)
            fund_id = request.data.get('fund_id')
            units_held = request.data.get('units_held')
            average_cost = request.data.get('average_cost')

            # Retrieve the fund and add it to the folio via the FundFolio relationship
            fund = Fund.objects.get(id=fund_id)
            FundFolio.objects.create(folio=folio, fund=fund, units_held=units_held, average_cost=average_cost,
                                     current_value=0)

            return Response({'message': 'Fund added to folio'}, status=status.HTTP_200_OK)
        except Folio.DoesNotExist:
            return Response({'error': 'Folio not found or does not belong to the user'},
                            status=status.HTTP_404_NOT_FOUND)
        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)


# New API for retrieving folio details including funds and performance
class FolioDetailView(generics.RetrieveAPIView):
    serializer_class = FolioSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'
    lookup_url_kwarg = 'folio_id'

    def get_queryset(self):
        return Folio.objects.filter(portfolio__user=self.request.user)
