from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, FormView
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

from funds.serializers import FundSerializer
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
                context['portfolio'] = user.portfolio
                context['folios'] = user.portfolio.folios.all()
            else:
                context['portfolio'] = None
                context['folios'] = []
            context['section'] = 'portfolio'

        # Funds Section
        elif section == 'funds':
            funds_queryset = Fund.objects.all()
            serializer = FundSerializer(funds_queryset, many=True)
            context['funds'] = serializer.data
            context['section'] = 'funds'

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
        print(request.user)
        if request.POST.get('old_password'):
                update_session_auth_hash(request, request.user)  # Keeps the user logged in
                context = self.get_context_data()
                context['password_change_done'] = True
                context['form'] = PasswordChangeForm(user=request.user)
                print(context['form'], context['password_change_done'])
                return self.render_to_response(context)

        return super().get(request, *args, **kwargs)
