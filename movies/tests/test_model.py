from django.test import TestCase

from citizen.tests.factories import SpeciesFactory

class TestSpeciesModel(TestCase):
    def test_str(self):
        species = SpeciesFactory(name='test_species')
        self.assertEqual(species.__str__(), 'test_species')