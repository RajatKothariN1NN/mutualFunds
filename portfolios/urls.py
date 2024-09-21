from django.urls import path
from .views import PortfolioView, FolioView, FundFolioView, CreateFolioView, BuySellFundView, FolioDetailView, DeleteFolioView

urlpatterns = [
    path('portfolio/<int:pk>/', PortfolioView.as_view(), name='portfolio-detail'),  # Existing Portfolio Detail
    path('folios/', FolioView.as_view(), name='folio-list'),  # List all folios for a user
    path('funds/', FundFolioView.as_view(), name='fund-folio-list'),  # List all funds in a folio (user specific)
    path('folios/create/', CreateFolioView.as_view(), name='create-folio'),  # Create new folio
    path('folios/transaction/', BuySellFundView.as_view(), name='add-fund-to-folio'),
    path('folios/<int:folio_id>/', FolioDetailView.as_view(), name='folio-detail'),  # Get details of a folio
    path('folios/delete/<int:id>/', DeleteFolioView.as_view(), name='delete-folio')

]

