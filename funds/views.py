from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render
from portfolios.models import Transaction
from .serializers import FundSerializer
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from funds.models import Fund
from django.core.cache import cache

class FundListView(generics.ListAPIView):
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        cache_key = 'fund_list'
        funds = cache.get(cache_key)
        if not funds:
            funds = Fund.objects.all()
            cache.set(cache_key, funds, timeout=60 * 15)  # Cache for 15 minutes
        return funds

    def get(self, request, *args, **kwargs):
        print('User:', request.user)
        return super().get(request, *args, **kwargs)

class FundDetailView(generics.RetrieveAPIView):
    queryset = Fund.objects.prefetch_related('folios')  # Assuming Fund has a foreign key to Folio
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        fund = self.get_object()  # Get the selected fund
        cache_key = f'transactions_{fund.id}_{request.user.id}'
        transactions = cache.get(cache_key)

        if transactions is None:
            transactions = Transaction.objects.filter(fund=fund, user=request.user)
            cache.set(cache_key, transactions, timeout=60 * 15)  # Cache for 15 minutes

        # Pagination
        paginator = Paginator(transactions, 5)  # Show 5 transactions per page
        page_number = request.GET.get('page')
        try:
            transactions_page = paginator.page(page_number)
        except PageNotAnInteger:
            transactions_page = paginator.page(1)
        except EmptyPage:
            transactions_page = paginator.page(paginator.num_pages)

        # Render the fund detail template with fund, folio, and paginated transactions
        return render(request, 'funds/fund_detail.html', {
            'fund': fund,
            'folio_id': kwargs['folio_id'],
            'transactions': transactions_page,
            'is_paginated': paginator.num_pages >= 1,
            'page_obj': transactions_page,  # Pass the page object for pagination links
        })

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

        # Pagination
        paginator = Paginator(queryset, 5)  # Show 5 funds per page
        page_number = request.GET.get('funds_page', 1)  # Use 'funds_page' for consistency
        try:
            funds_page = paginator.page(page_number)
        except PageNotAnInteger:
            funds_page = paginator.page(1)
        except EmptyPage:
            funds_page = paginator.page(paginator.num_pages)

        # Use the serializer on the paginated funds
        serializer = self.get_serializer(funds_page, many=True)

        context = {
            'funds': serializer.data,  # Pass the serialized paginated funds
            'folio_id': folio_id,
            'is_funds_paginated': paginator.num_pages > 1,
            'available_funds_page': funds_page,  # Pass the page object for pagination links
        }

        return render(request, self.template_name, context)
class UpdateFundValueView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, fund_id, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_staff and not request.user.is_superuser:
            return Response({'error': 'You do not have permission to perform this action.'}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Retrieve the fund to update
            fund = Fund.objects.get(id=fund_id)
            new_value = request.data.get('current_value')

            # Update the current value of the fund
            fund.nav = new_value
            fund.save()

            # Invalidate cache for fund list to ensure updates are reflected
            cache.delete('fund_list')

            return Response({'message': 'Fund value updated successfully'}, status=status.HTTP_200_OK)

        except Fund.DoesNotExist:
            return Response({'error': 'Fund not found'}, status=status.HTTP_404_NOT_FOUND)
