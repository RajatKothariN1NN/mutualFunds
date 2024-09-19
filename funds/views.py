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