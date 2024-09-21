from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.core.cache import cache
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from funds.serializers import FundSerializer
from portfolios.models import Folio, Portfolio
from users.forms import ProfileForm
from funds.models import Fund


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

                if not portfolio:
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
