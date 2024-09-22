from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from requests import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.pagination import PageNumberPagination
from django.db.models import DecimalField, IntegerField
from django.db.models.functions import Cast, Substr, Length
from decimal import Decimal
from funds.serializers import FundSerializer, ThemeSerializer, RiskProfileSerializer, FundTypeSerializer
from portfolios.models import Folio, Portfolio
from users.forms import ProfileForm
from funds.models import Fund, FundType, RiskProfile, Theme
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import UserPreferences
from funds.serializers import  FundSerializer
from users.serializers import UserPreferencesSerializer



def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')  # Redirect to the dashboard if the user is authenticated
    return render(request, 'home.html')


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        section = self.request.GET.get('section', 'portfolio')
        context['profile_pic'] = user.profile_pic.url if user.profile_pic else '/static/images/default_profile_pic.png'

        # Profile Section
        if section == 'profile':
            context['form'] = ProfileForm(instance=user)
            context['section'] = 'profile'

        # Portfolio Section
        elif section == 'portfolio':
            if hasattr(user, 'portfolio'):
                cache_key = f'portfolio_{user.id}'
                portfolio = cache.get(cache_key)
                #
                if portfolio is None:
                    portfolio = Portfolio.objects.select_related('user').prefetch_related('folios__funds').get(
                        user=user)
                    cache.set(cache_key, portfolio, timeout=60 * 15)  # Cache the portfolio for 15 minutes

                context['portfolio'] = portfolio
                folios = portfolio.folios.all()  # Fetch funds for each folio

                # Check if a specific folio is being requested
                # Pagination
                paginator = Paginator(folios, 5)  # Show 5 folios per page
                page_number = self.request.GET.get('page')
                try:
                    folios_page = paginator.page(page_number)
                except PageNotAnInteger:
                    folios_page = paginator.page(1)
                except EmptyPage:
                    folios_page = paginator.page(paginator.num_pages)

                context['folios'] = folios_page  # Use the paginated list
                context['paginator'] = paginator
                context['page_number'] = page_number

                folio_id = self.request.GET.get('folio_id')
                if folio_id:
                    try:
                        context['folio'] = portfolio.folios.get(id=folio_id)
                    except Folio.DoesNotExist:
                        context['folio'] = None
            else:
                context['portfolio'] = None
                context['folios'] = []
            context['section'] = 'portfolio'

        # Funds Section
        elif section == 'funds':
            funds_queryset = Fund.objects.all()
            paginator = Paginator(funds_queryset, 5)  # Show 5 funds per page
            page_number = self.request.GET.get('funds_page')

            try:
                funds_page = paginator.page(page_number)
            except PageNotAnInteger:
                funds_page = paginator.page(1)
            except EmptyPage:
                funds_page = paginator.page(paginator.num_pages)

            # Serialize the paginated funds
            serializer = FundSerializer(funds_page, many=True)

            # Pass the serialized data for rendering the funds and the paginated queryset for pagination logic
            context['funds'] = serializer.data  # Serialized data for funds
            context['funds_page'] = funds_page  # Paginated QuerySet for pagination logic
            context['funds_paginator'] = paginator
            context['funds_page_number'] = page_number
            context['section'] = 'funds'
            context['is_paginated'] = funds_page.has_other_pages()  # Ensure pagination status


        # Password Change Section
        elif section == 'password_change':
            context['form'] = PasswordChangeForm(user=self.request.user)
            context['section'] = 'password_change'

        # Password Change Success
        elif section == 'password_change_done':
            context['section'] = 'password_change'
            context['password_change_done'] = True

        return context

    def post(self, request, *args, **kwargs):
        # Password change handling
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keeps the user logged in
            context = self.get_context_data()
            context['password_change_done'] = True
            context['form'] = PasswordChangeForm(user=request.user)  # Reset form
            return self.render_to_response(context)

        # If form is not valid, re-render with errors
        context = self.get_context_data()
        context['form'] = form  # Pass the form with errors
        return self.render_to_response(context)


class FundTypeListView(APIView):
    def get(self, request):
        cache_key = 'fund_types'
        fund_types = cache.get(cache_key)

        if fund_types is None:
            fund_types = FundType.objects.all()
            serializer = FundTypeSerializer(fund_types, many=True)
            fund_types_data = serializer.data
            cache.set(cache_key, fund_types_data, timeout=3600)  # Cache for 1 hour
        else:
            fund_types_data = fund_types

        return Response(fund_types_data, status=status.HTTP_200_OK)


class RiskProfileListView(APIView):
    def get(self, request):
        cache_key = 'risk_profiles'
        risk_profiles = cache.get(cache_key)

        if risk_profiles is None:
            risk_profiles = RiskProfile.objects.all()
            serializer = RiskProfileSerializer(risk_profiles, many=True)
            risk_profiles_data = serializer.data
            cache.set(cache_key, risk_profiles_data, timeout=3600)  # Cache for 1 hour
        else:
            risk_profiles_data = risk_profiles

        return Response(risk_profiles_data, status=status.HTTP_200_OK)

class ThemeListView(APIView):
    def get(self, request):
        cache_key = 'themes'
        themes = cache.get(cache_key)

        if themes is None:
            themes = Theme.objects.all()
            serializer = ThemeSerializer(themes, many=True)
            cache.set(cache_key, serializer.data, timeout=3600)

        return Response(cache.get(cache_key), status=status.HTTP_200_OK)


class UserPreferencesView(generics.CreateAPIView):
    serializer_class = UserPreferencesSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        preferences_data = request.data
        user_preferences, created = UserPreferences.objects.get_or_create(user=user)
        serializer = self.get_serializer(user_preferences, data=preferences_data, partial=True)

        if serializer.is_valid():
            serializer.save()
            # Invalidate the cache for recommended funds when preferences are updated
            cache.delete(f'recommended_funds_{user.id}')
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class RecommendedFundsPagination(PageNumberPagination):
    page_size = 5  # Number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 10  # Maximum items per page

class RecommendedFundsView(ListAPIView):
    serializer_class = FundSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = RecommendedFundsPagination

    def get_queryset(self):
        user = self.request.user
        folio_id = self.kwargs.get('folio_id')

        # Check cache first
        cache_key = f'recommended_funds_{user.id}'
        recommended_funds = cache.get(cache_key)

        if True:
            user_preferences = UserPreferences.objects.filter(user=user).first()
            filters = {}

            if user_preferences:
                # Build filters based on user preferences
                if user_preferences.fund_types:
                    filters['fund_type__in'] = user_preferences.fund_types
                if user_preferences.risk_profiles:
                    filters['risk_profile__in'] = user_preferences.risk_profiles
                if user_preferences.themes:
                    filters['themes__in'] = user_preferences.themes

            # Annotate the queryset to extract numeric values from 'investment_duration' and 'expected_returns'
            queryset = Fund.objects.annotate(
                # Convert 'investment_duration' (e.g., "5 years") to an integer
                investment_duration_numeric=Cast(
                    Substr('investment_duration', 1, Length('investment_duration') - 6),  # Remove " years"
                    output_field=IntegerField()
                ),
                # Convert 'expected_returns' (e.g., "10%") to a decimal
                expected_returns_decimal=Cast(
                    Substr('expected_returns', 1, Length('expected_returns') - 1),  # Remove "%"
                    output_field=DecimalField(max_digits=5, decimal_places=2)
                )
            )

            # Apply the filters
            if user_preferences and user_preferences.investment_duration:
                filters['investment_duration_numeric'] = int(user_preferences.investment_duration)
            if user_preferences and user_preferences.expected_returns is not None:
                filters['expected_returns_decimal__gte'] = Decimal(user_preferences.expected_returns)

            # Apply filtering and exclude funds already in the folio
            recommended_funds = queryset.filter(
                **filters
            ).exclude(folios__id=folio_id)

            # Cache the result as serialized data
            cache.set(cache_key, list(recommended_funds.values()), timeout=3600)

        return recommended_funds

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        # Pagination
        paginator = self.pagination_class()
        page_number = request.GET.get('recommended_page', 1)
        paginated_funds = paginator.paginate_queryset(queryset, request)

        return paginator.get_paginated_response(self.get_serializer(paginated_funds, many=True).data)
