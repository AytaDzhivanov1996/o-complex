import requests
import os

from django.shortcuts import render
from django.http import JsonResponse

from config import settings
from .models import City, SearchHistory
from dotenv import load_dotenv

def get_weather(city_name):
    env_path = settings.env_path
    load_dotenv(dotenv_path=env_path, override=True)
    api_key = os.getenv('API_KEY')
    api_url = f'http://api.weatherapi.com/v1/forecast.json?key={api_key}&q={city_name}&days=7&aqi=no&alerts=no'
    response = requests.get(api_url)
    return response.json()

def index(request):
    weather = {}
    if request.method == 'POST':
        city_name = request.POST['city']
        city, created = City.objects.get_or_create(name=city_name)
        city.query_count += 1
        city.save()

        request.session['last_city'] = city_name
        weather_data = get_weather(city_name)
        SearchHistory.objects.create(city=city)
        for elem in weather_data['forecast']['forecastday']:
            weather[elem['date']] = elem['day']['maxtemp_c']
        return render(request, 'weather/index.html', {'weather': weather, 'city': city_name})

    last_city = request.session.get('last_city')
    if last_city:
        weather_data = get_weather(last_city)
        for elem in weather_data['forecast']['forecastday']:
            weather[elem['date']] = elem['day']['maxtemp_c']
        return render(request, 'weather/index.html', {'weather': weather, 'city': last_city})

    return render(request, 'weather/index.html')

def history_city_count(request):
    history = City.objects.all()
    return JsonResponse([{'city': h.name, 'query_count': h.query_count} for h in history], safe=False)

def history(request):
    history = SearchHistory.objects.all()
    return JsonResponse([{'city': h.city.name, 'timestamp': h.timestamp} for h in history], safe=False)

def autocomplete(request):
    search = request.GET.get('q', '')
    cities = City.objects.filter(name__icontains=search)
    return JsonResponse([city.name for city in cities], safe=False)
