from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
try:
    from rest_framework_simplejwt.tokens import RefreshToken
except ModuleNotFoundError:
    # Handle the error or ignore it
    pass
from rest_framework.response import Response
from .models import User
from .serializers import UserSerializer
from django.contrib.auth import logout, login

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/register.html')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login')  # Redirect on successful registration
        return render(request, 'users/register.html', {'errors': serializer.errors, 'request': request})

class LoginView(generics.CreateAPIView):
    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard')
        return render(request, 'users/login.html')

    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        password = request.POST.get('password')
        cache_key = f'login_attempts_{email}'
        max_attempts = 5  # Set max attempts before blocking

        attempts = cache.get(cache_key, 0)  # Get current attempt count from cache

        if attempts >= max_attempts:
            return render(request, 'users/login.html', {'error': 'Too many login attempts. Please try again later.'})

        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                response = redirect('dashboard')

                response.set_cookie('refresh', str(refresh))
                response.set_cookie('access', str(refresh.access_token))
                login(request, user)
                cache.delete(cache_key)  # Clear login attempts on success
                return response
            else:
                cache.set(cache_key, attempts + 1,
                          timeout=300)  # Increment attempt count, block after 5 failed attempts for 5 mins
                return render(request, 'users/login.html', {'error': 'Invalid password'})
        except User.DoesNotExist:
            return render(request, 'users/login.html', {'error': 'User does not exist'})
        except Exception as e:
            return render(request, 'users/login.html', {'error': str(e)})


class LogoutView(LoginRequiredMixin, generics.GenericAPIView):
    def get_serializer_class(self):
        return None  # Override this to avoid the error

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get('refresh_token')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()  # Blacklist the refresh token
            request.session.flush()  # Clear the session
            return Response({'message': 'Successfully logged out'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProfileView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    context_object_name = 'user'

    def get_object(self):
        cache_key = f'user_profile_{self.request.user.id}'
        user = cache.get(cache_key)

        if user is None:
            user = self.request.user  # Fetch the logged-in user
            cache.set(cache_key, user, timeout=60 * 15)  # Cache for 15 minutes

        return user

class UpdateProfileView(LoginRequiredMixin, generics.UpdateAPIView):
    http_method_names = ['post', 'patch']
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        user_id = self.request.data.get('user_id')
        if user_id:
            return User.objects.get(id=user_id)
        return self.request.user

    def perform_update(self, serializer):
        profile_pic = self.request.FILES.get('profile_pic')
        phone_number = self.request.data.get('phone_number')
        PAN = self.request.data.get('PAN')

        user_data = {
            'profile_pic': profile_pic,
            'phone_number': phone_number,
            'PAN': PAN
        }

        if 'username' in self.request.data:
            user_data['username'] = self.request.data['username']
        if 'email' in self.request.data:
            user_data['email'] = self.request.data['email']

        serializer.save(**user_data)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(self.object, data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return redirect(reverse('dashboard') + '?section=profile')  # Redirect after success
