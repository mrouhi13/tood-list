from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class AuthAPITests(APITestCase):

    def setUp(self):
        pass

    def test_login(self):
        user_1 = User.objects.create_user(username='user_1',
                                          password='1234')
        url = reverse('api_v1:users:access-token')
        data = {
            'username': user_1.username,
            'password': '1234',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        self.assertTrue('refresh' in response.data)

    def test_login_refresh(self):
        user_1 = User.objects.create_user(username='user_1',
                                          password='1234')
        obtain_token_url = reverse('api_v1:users:access-token')
        credentials = {
            'username': user_1.username,
            'password': '1234',
        }
        auth_response = self.client.post(obtain_token_url, credentials,
                                         format='json')
        url = reverse('api_v1:users:refresh-token')
        data = {
            'refresh': auth_response.data['refresh'],
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)

    def test_register(self):
        url = reverse('api_v1:users:register')
        data = {
            'username': 'test',
            'password': 'B:3ZF$cv@zV}awT2',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('access' in response.data)

    def test_register_with_duplicate_username(self):
        User.objects.create_user('test')
        url = reverse('api_v1:users:register')
        data = {
            'username': 'test',
            'password': 'B:3ZF$cv@zV}awT2',
        }
        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['username'][0],
                         'An account with this username is already '
                         'registered.')
