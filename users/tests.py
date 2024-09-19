from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status

class UserModelTests(TestCase):
    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            email='test@example.com',
            username='testuser',
            phone_number='1234567890',
            PAN='ABCDE1234F',
            password='password123'
        )
        self.assertEqual(user.email, 'test@example.com')
        self.assertTrue(user.check_password('password123'))
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        superuser = User.objects.create_superuser(
            email='superuser@example.com',
            username='superuser',
            phone_number='0987654321',
            PAN='XYZAB5678C',
            password='password123'
        )
        self.assertEqual(superuser.email, 'superuser@example.com')
        self.assertTrue(superuser.is_superuser)
        self.assertTrue(superuser.is_staff)

# users/tests/test_views.py

class RegisterViewTests(APITestCase):
    def test_register(self):
        url = '/api/register/'
        data = {
            'email': 'newuser@example.com',
            'username': 'newuser',
            'phone_number': '1112223333',
            'PAN': 'ABCD1234E',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], 'newuser@example.com')


class LoginViewTests(APITestCase):
    def setUp(self):
        self.user = {
            'email': 'loginuser@example.com',
            'username': 'loginuser',
            'phone_number': '4445556666',
            'PAN': 'XYZAB1234C',
            'password': 'password123'
        }
        self.client.post('/api/register/', self.user, format='json')

    def test_login(self):
        url = '/api/login/'
        data = {
            'email': self.user['email'],
            'password': self.user['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

# users/tests/test_views.py
class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = {
            'email': 'logoutuser@example.com',
            'username': 'logoutuser',
            'phone_number': '7778889999',
            'PAN': 'LMNOP5678Q',
            'password': 'password123'
        }
        response = self.client.post('/api/register/', self.user, format='json')
        self.token = self.client.post('/api/login/', {
            'email': self.user['email'],
            'password': self.user['password']
        }, format='json').data['refresh']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_logout(self):
        url = '/api/logout/'
        response = self.client.post(url, {'refresh_token': self.token}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], 'Successfully logged out')

# users/tests/test_views.py
class UpdateProfileViewTests(APITestCase):
    def setUp(self):
        self.user = {
            'email': 'updateuser@example.com',
            'username': 'updateuser',
            'phone_number': '2223334444',
            'PAN': 'EFGHI6789R',
            'password': 'password123'
        }
        response = self.client.post('/api/register/', self.user, format='json')
        self.token = self.client.post('/api/login/', {
            'email': self.user['email'],
            'password': self.user['password']
        }, format='json').data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_update_profile(self):
        url = '/api/profile/update/'
        data = {'username': 'updateduser'}
        response = self.client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'updateduser')
