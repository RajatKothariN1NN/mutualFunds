from django.urls import path
from .views import FundListView, FundDetailView, AvailableFundListView

urlpatterns = [
    path('', FundListView.as_view(), name='fund-list'),
    path('<int:pk>/', FundDetailView.as_view(), name='fund-detail'),
    path('available/<int:folio_id>/', AvailableFundListView.as_view(), name='available-fund-list'),

]
