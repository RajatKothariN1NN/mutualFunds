from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Fund
from .serializers import FundSerializer

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


class AvailableFundListView(generics.ListAPIView):
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        folio_id = self.kwargs.get('folio_id')
        return Fund.objects.exclude(folios__id=folio_id)


from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from funds.models import Fund

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
