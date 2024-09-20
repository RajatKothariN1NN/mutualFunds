from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import home, DashboardView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),  # Route to home view
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('profile/', DashboardView.as_view(), name='profile'),

    path('api/auth/', include('users.urls')),
    path('api/funds/', include('funds.urls')),
    path('api/portfolios/', include('portfolios.urls')),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

