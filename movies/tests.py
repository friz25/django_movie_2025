from django.test import TestCase

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from models import Category, Movie

class MoviesTests(APITestCase):
    def test_movies_list(self):
        response = self.client.get('movies_list')
        print(response)
    # def test_create_account(self):
        # """
        # Ensure we can create a new account object.
        # """
        # url = reverse('account-list')
        # data = {'name': 'DabApps'}
        # response = self.client.post(url, data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertEqual(Account.objects.count(), 1)
        # self.assertEqual(Account.objects.get().name, 'DabApps')
