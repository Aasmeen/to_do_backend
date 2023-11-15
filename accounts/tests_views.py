import json
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

class RegisterAPITestCase(APITestCase):
    def setUp(self):
        self.url = '/api/register/'
    
    def test_register_user(self):
        # Test POST request to register user
        new_data = {
            'username': 'user',
            'first_name': 'User',
            'last_name': 'Test' ,
            'password': 'password@1',
            'password2': 'password@1'
        }
        response = self.client.post(self.url, data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['first_name'], new_data['first_name'])
        self.assertTrue(User.objects.filter(username=new_data['username']).exists())
        
        token = Token.objects.filter(user__username=new_data['username'])
        self.assertTrue(token.exists())
        self.assertEqual(response.data['token'], token.values('key').first().get('key'))
    
    def test_common_password_error(self):
        # Test POST request to register user with common password
        new_data = {
            'username': 'user',
            'first_name': 'User',
            'last_name': 'Test' ,
            'password': 'password',
            'password2': 'password'
        }
        response = self.client.post(self.url, data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('password' in response.data)
    
    def test_existing_username_error(self):
        # Test POST request to register user with existing username
        new_data = {
            'username': 'user',
            'first_name': 'User',
            'last_name': 'Test' ,
            'password': 'password@1',
            'password2': 'password@1'
        }
        response = self.client.post(self.url, data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.post(self.url, data=json.dumps(new_data), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue('username' in response.data)


class LogoutAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='password')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        self.url = '/api/logout/'
    
    def test_logout(self):
        # Test POST request to logout user
        response = self.client.post(self.url, data=json.dumps({}), content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Token.objects.filter(user__username=self.user.username).first())

        