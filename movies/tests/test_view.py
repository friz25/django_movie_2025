from django.db import connection
from django.urls import reverse
from rest_framework.test import APITestCase
from movies.models import Category, Actor, Movie

class TestCitizenListAPIView(APITestCase):
    def test_missing_species(self):
        self.spepecies_rabbit = Species.objects.create(name='rabbit')
        self.citizen_judy = Citizen.objects.create(
            name= ''
        )
        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM actor where id = %s', [self.actor.id])