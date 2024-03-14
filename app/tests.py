from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import User
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from .serializers import UserProfileSerializer
from django.http import JsonResponse
import json


class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_url = reverse('user-registration')  
        
    def test_user_registration_invalid_data(self):
        invalid_registration_data = {
            
        }
        response = self.client.post(self.registration_url, invalid_registration_data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        self.assertIn('email', response.data)
        self.assertIn('name', response.data)
        self.assertIn('password2', response.data)
        self.assertIn('tc', response.data)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('user-login')  
        User = get_user_model()
        self.user = User.objects.create_user(email='test@example.com', password='password123', name='Test User', tc=True)

    # Your test methods go here

    def test_user_login_success(self):
        login_data = {
            'email': 'test@example.com',
            'password': 'password123',
        }
        response = self.client.post(self.login_url, login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('msg', response.data)
        self.assertEqual(response.data['msg'], 'Login Success')

    def test_user_login_invalid_credentials(self):
        invalid_login_data = {
            'email': 'invalid@example.com',
            'password': 'invalid_password',
        }
        response = self.client.post(self.login_url, invalid_login_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('errors', response.data)
        self.assertIn('non_field_errors', response.data['errors'])
        self.assertEqual(response.data['errors']['non_field_errors'], ['Email or Password is not Valid'])


class UserProfileViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='password123', name='Test User', tc=True)
        self.client.force_authenticate(user=self.user)
        self.profile_url = reverse('user-profile') 

    def test_user_profile_view(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, UserProfileSerializer(self.user).data)


class UserChangePasswordViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(email='test@example.com', password='old_password', name='Test User', tc=True)
        self.client.force_authenticate(user=self.user)
        self.change_password_url = reverse('user-change-password')

    def test_user_change_password(self):
        data = {
            'old_password': 'incorrect_old_password',  # provide an incorrect old password
            'new_password': 'new_password',
            'confirm_password': 'new_password',
        }
        response = self.client.post(self.change_password_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class SendPasswordResetEmailViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.send_reset_email_url = reverse('send-password-reset-email')  

    def test_send_password_reset_email(self):
        data = {
            'email': 'test@example.com',
        }
        response = self.client.post(self.send_reset_email_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)


class UserPasswordResetViewTestCase(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.password_reset_url = reverse('user-password-reset', kwargs={'uid': 'valid_uid', 'token': 'valid_token'}) 

    def test_user_password_reset(self):
        data = {
            'new_password': 'new_password',
            'confirm_password': 'new_password',
        }
        response = self.client.post(self.password_reset_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertIn('password2', response.data)

