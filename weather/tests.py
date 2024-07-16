from django.test import TestCase
from django.urls import reverse
from .models import City, SearchHistory

class WeatherAppTests(TestCase):

    def test_index(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weather App")

    def test_search_city(self):
        response = self.client.post(reverse('index'), {'city': 'Madrid'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Weather for Madrid")
        city = City.objects.get(name='Madrid')
        self.assertEqual(city.query_count, 1)
        self.assertEqual(SearchHistory.objects.count(), 1)

