from decimal import Decimal

from django.http import HttpResponseRedirect
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from rest_framework import generics, status
from rest_framework.generics import DestroyAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Portfolio, Folio, FundFolio, Transaction
from .serializers import PortfolioSerializer, FolioSerializer, FundFolioSerializer, BuySellFundSerializer
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
class CreateFolioView(LoginRequiredMixin , generics.CreateAPIView):
    serializer_class = FolioSerializer

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

    def get(self, request, *args, **kwargs):
        folio = self.get_object()  # Get the specific folio instance
        serializer = self.get_serializer(folio)

        # Render the template with folio details
        return render(request, 'portfolios/folio-detail.html', {
            'folio': serializer.data,  # Pass the serialized folio data to the template
        })




class BuySellFundView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BuySellFundSerializer

    def post(self, request, *args, **kwargs):
        print(request.data)

        transaction_type = request.data.get('transaction_type')
        fund_id = request.data.get('fund_id')
        try:
            units = Decimal(request.data.get('units', 0))  # Default to 0 if None
            price_per_unit = Decimal(request.data.get('price_per_unit', 0))  # Default to 0 if None
        except (ValueError, TypeError):
            return Response({'error': 'Invalid units or price per unit'}, status=status.HTTP_400_BAD_REQUEST)

        folio_id = request.data.get('folio_id')
        if units <= 0 or price_per_unit <= 0:
            return Response({'error': 'Units and price per unit must be greater than zero'},
                            status=status.HTTP_400_BAD_REQUEST)

        if transaction_type not in ['buy', 'sell']:
            return Response({'error': 'Invalid transaction type'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fund = Fund.objects.get(id=fund_id)
            folio = Folio.objects.get(id=folio_id, portfolio__user=request.user)

            # Calculate total value of the transaction
            total_value = units * price_per_unit
            print("I am here")
            fund_folio, created = FundFolio.objects.get_or_create(folio=folio, fund=fund)
            print("I reached here")
            if transaction_type == 'buy':
                # Check if the fund is already in the folio


                if not created:
                    # If the fund already exists in the folio, update units and average cost
                    total_units = fund_folio.units_held + units
                    total_cost = (fund_folio.units_held * fund_folio.average_cost) + total_value
                    fund_folio.average_cost = total_cost / total_units
                    fund_folio.units_held = total_units
                else:
                    # If it's a new fund in the folio, set the initial units and average cost
                    fund_folio.units_held = units
                    fund_folio.average_cost = price_per_unit

                fund_folio.save()

            elif transaction_type == 'sell':
                # Check if the user has enough units to sell
                if fund_folio.units_held < units:
                    return Response({'error': 'Not enough units to sell'}, status=status.HTTP_400_BAD_REQUEST)
                total_cost = (fund_folio.units_held * fund_folio.average_cost) - total_value
                fund_folio.units_held -= units
                if fund_folio.units_held == 0:
                    # If no units left, delete the fund from the folio
                    fund_folio.delete()
                else:
                    fund_folio.average_cost = total_cost/fund_folio.units_held

                    fund_folio.save()

            # Create a transaction record
            Transaction.objects.create(
                user=request.user,
                fund=fund,
                portfolio=folio.portfolio,
                units=units,
                transaction_type=transaction_type,
                price_per_unit=price_per_unit
            )
            return redirect('folio-detail', folio_id=folio.id)

        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
        except Folio.DoesNotExist:
            return Response({'error': 'Folio not found or does not belong to the user'},
                            status=status.HTTP_404_NOT_FOUND)



class DeleteFolioView(DestroyAPIView):
    queryset = Folio.objects.all()  # Specify the queryset for Folio
    lookup_field = 'id'
    serializer_class = FolioSerializer

    def get(self, request, *args, **kwargs):
        """
        Handle GET request for deletion instead of DELETE.
        """
        # Call the destroy method when a POST request is made
        return self.delete(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        folio = self.get_object()  # Get the folio instance
        # Check if the folio has any invested amount
        if folio.total_invested_amount() == 0:
            super().destroy(request, *args, **kwargs)  # Proceed with deletion
            return HttpResponseRedirect(reverse('dashboard'))  # Redirect to dashboard

            # Return a response if deletion is not allowed
        return Response(
            {"detail": "Folio cannot be deleted because it has invested amount."},
            status=status.HTTP_400_BAD_REQUEST)