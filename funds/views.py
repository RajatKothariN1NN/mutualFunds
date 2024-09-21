from django.shortcuts import render
from portfolios.models import Transaction
from .serializers import FundSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from funds.models import Fund


class FundListView(generics.ListAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        print('User:', request.user)
        return super().get(request, *args, **kwargs)

class FundDetailView(generics.RetrieveAPIView):
    queryset = Fund.objects.all()
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fund = self.get_object()  # Get the selected fund
        transactions = Transaction.objects.filter(fund=fund, user=request.user)  # Get user's transactions for the fund

        # Render the fund detail template with fund, folio, and transactions
        return render(request, 'funds/fund_detail.html', {'fund': fund,'folio_id': kwargs['folio_id'], 'transactions': transactions})


class AvailableFundListView(generics.ListAPIView):
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]
    template_name = 'funds/add_fund_to_folio.html'

    def get_queryset(self):
        folio_id = self.kwargs.get('folio_id')
        return Fund.objects.exclude(folios__id=folio_id)

    def get(self, request, *args, **kwargs):
        folio_id = self.kwargs.get('folio_id')
        queryset = self.get_queryset()

        # Use the serializer here
        serializer = self.get_serializer(queryset, many=True)

        context = {
            'funds': serializer.data,
            'folio_id': folio_id,
        }

        return render(request, self.template_name, context)


class UpdateFundValueView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, fund_id, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_staff and request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Retrieve the fund to update
            fund = Fund.objects.get(id=fund_id)
            new_value = request.data.get('current_value')

            # Update the current value of the fund
            fund.nav = new_value
            fund.save()

            return Response({'message': 'Fund value updated successfully'}, status=status.HTTP_200_OK)

        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
