from django.shortcuts import render
import requests
from datetime import datetime



def index(request):
    try:
        if request.method == 'POST':
            API_KEY = '7828fd0a61910b92a261914b6ee796e8'
            city_name = request.POST.get('city')
            url = f'https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={API_KEY}&units=metric'
            response = requests.get(url).json()
            current_time = datetime.now()
            formatted_time = current_time.strftime("%A, %B %d %Y, %I:%M:%S %p")
           
            city_weather_update = {
                'city': city_name,
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
                'temperature': 'Temperature: ' + str(response['main']['temp']) + ' °C',
                'country_code': response['sys']['country'],
                'wind': 'Wind: ' + str(response['wind']['speed']) + ' km/h',
                'humidity': 'Humidity: ' + str(response['main']['humidity']) + '%',
                'sea_level': 'Sea Level: ' + str(response['main'].get('sea_level', 'N/A')) + ' hPa',
                'sunrise': 'Sunrise: ' + datetime.fromtimestamp(response['sys']['sunrise']).strftime('%I:%M:%S %p'),
                'sunset': 'Sunset: ' + datetime.fromtimestamp(response['sys']['sunset']).strftime('%I:%M:%S %p'),
                'time': formatted_time
            }

            if 'rain' in response:
                if '3h' in response['rain']:
                    city_weather_update['water_level'] = 'Water Level: ' + str(response['rain']['3h']) + ' mm'
                elif '1h' in response['rain']:
                    city_weather_update['water_level'] = 'Water Level: ' + str(response['rain']['1h']) + ' mm'
                else:
                    city_weather_update['water_level'] = 'Water Level: N/A'
            else:
                city_weather_update['water_level'] = 'Water Level: N/A'

        else:
            city_weather_update = {}

        context = {'city_weather_update': city_weather_update}
        return render(request, 'weatherupdates/home.html', context)
    except:
        return render(request, 'weatherupdates/404.html')
