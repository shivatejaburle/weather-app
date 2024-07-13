from django.shortcuts import render
from django.conf import settings

# Import json to load JSON Data to Python Dictionary 
import json

# To make a request to API
import urllib.request

from django.views import View
from weather.forms import WeatherByCityForm
# Create your views here.

class IndexView(View):
    template_name = 'weather/index.html'

    def get(self, request):
        form = WeatherByCityForm()
        context = {'form':form}
        return render(request, self.template_name, context)
    
    def post(self, request):
        get_city = request.POST['city']
        city = get_city.replace(" ", "%20")
        print(city)
        form = WeatherByCityForm()
        try:
            # Get your  API Key from OpenWeather and replace the key below with yours
            # https://openweathermap.org/

            # Get JSON data from API
            api_url = str('http://api.openweathermap.org/data/2.5/weather?q='+city+'&appid='+settings.WEATHER_API_KEY)
            source_data = urllib.request.urlopen(api_url).read()
            
            # Convert JSON Data to a Python Dictionary
            list_of_data = json.loads(source_data)

            # Kelvin to Celsius Conversion
            temperature_c = round(float(list_of_data['main']['temp']) - 273.15, 2)
            temperature_feels_like = round(float(list_of_data['main']['feels_like']) - 273.15, 2)

            # Get data from list_of_date
            weather_data = {
                'city_name' : str(list_of_data['name']),
                'country_code' : str(list_of_data['sys']['country']),
                'lat' : str(list_of_data['coord']['lat']),
                'lon' : str(list_of_data['coord']['lon']),
                'temperature' : str(temperature_c) + '°C',
                'feels_like' : str(temperature_feels_like) + '°C',
                'pressure' : str(list_of_data['main']['pressure']),
                'humidity' : str(list_of_data['main']['humidity']),
                'wind_speed' : str(list_of_data['wind']['speed']),
                'weather_description' : str(list_of_data['weather'][0]['description']),
                'icon' : str(list_of_data['weather'][0]['icon']),

            }
            context = {'form':form, 'weather_data':weather_data}
        except:
            print("City not found")
            weather_data = {
                'error' : city + ' city not found. Please enter a valid city name.',
            }
            context = {'form':form, 'weather_data':weather_data}

        return render(request, self.template_name, context)