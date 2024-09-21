# middleware.py
import re
from django.utils.deprecation import MiddlewareMixin

class TokenAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header:
            # Extract the token from cookies if it's not already in the header
            access_token = request.COOKIES.get('access')
            if access_token:
                request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
