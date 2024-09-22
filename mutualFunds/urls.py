from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, DashboardView, FundTypeListView, RiskProfileListView, ThemeListView, UserPreferencesView, \
    RecommendedFundsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Route to home view
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', DashboardView.as_view(), name='profile'),
    path('fund-types/', FundTypeListView.as_view(), name='fund-types'),
    path('risk-profiles/', RiskProfileListView.as_view(), name='risk-profiles'),
    path('themes/', ThemeListView.as_view(), name='themes'),
    path('user-preferences/', UserPreferencesView.as_view(), name='user-preferences'),
    path('recommended-funds/<int:folio_id>/', RecommendedFundsView.as_view(), name='recommended-funds-list'),
    path('api/auth/', include('users.urls')),
    path('api/funds/', include('funds.urls')),
    path('api/portfolios/', include('portfolios.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

