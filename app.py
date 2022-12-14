import os
import requests

from pprint import PrettyPrinter
from datetime import datetime, timedelta
from dotenv import load_dotenv
from flask import Flask, render_template, request, send_file


################################################################################
## SETUP
################################################################################

app = Flask(__name__)

# Get the API key from the '.env' file
load_dotenv()

pp = PrettyPrinter(indent=4)

API_KEY = os.getenv('API_KEY')
API_URL = 'http://api.openweathermap.org/data/2.5/weather'


################################################################################
## ROUTES
################################################################################

@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""
    context = {
        'min_date': (datetime.now() - timedelta(days=5)),
        'max_date': datetime.now()
    }
    return render_template('home.html', **context)

def get_letter_for_units(units):
    """Returns a shorthand letter for the given units."""
    return 'F' if units == 'imperial' else 'C' if units == 'metric' else 'K'

@app.route('/results')
def results():
    """Displays results for current weather conditions."""
    # TODO: Use 'request.args' to retrieve the city & units from the query
    # parameters.

    city = request.args.get('city')
    units = request.args.get('units')

    params = {
        # TODO: Enter query parameters here for the 'appid' (your api key),
        # the city, and the units (metric or imperial).
        # See the documentation here: https://openweathermap.org/current
        # https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API key}
        # http://api.openweathermap.org/data/2.5/weather?q=YOUR_CITY_HERE&appid=YOUR_APP_ID&units=imperial
        "q": city,
        'appid': API_KEY,
        "units": units
    }

    result_json = requests.get(API_URL, params=params).json()

    # Uncomment the line below to see the results of the API call!
    print(result_json)

    # TODO: Replace the empty variables below with their appropriate values.
    # You'll need to retrieve these from the result_json object above.

    # For the sunrise & sunset variables, I would recommend to turn them into
    # datetime objects. You can do so using the `datetime.fromtimestamp()` 
    # function.
    date = datetime.now()
    sunrise = datetime.fromtimestamp(result_json['sys']['sunrise'])
    sunset = datetime.fromtimestamp(result_json['sys']['sunset'])
    context = {
        'date': date.strftime("%D %H:%M:%S"),
        'city': result_json['name'],
        'description': result_json['weather'][0]['description'],
        'temp': result_json['main']['temp'],
        'humidity': result_json['main']['humidity'],
        'wind_speed': result_json['wind']['speed'],
        'sunrise': sunrise.strftime("%H:%M:%S"),
        'sunset': sunset.strftime("%H:%M:%S"),
        'units_letter': get_letter_for_units(units)
    }

    return render_template('results.html', **context)


@app.route('/comparison_results')
def comparison_results():
    """Displays the relative weather for 2 different cities."""
    # TODO: Use 'request.args' to retrieve the cities & units from the query
    # parameters.
    city1 = request.args.get('city1')
    city2 = request.args.get('city2')
    units = request.args.get('units')

    # TODO: Make 2 API calls, one for each city. HINT: You may want to write a 
    # helper function for this!
    city1_params = {"q": city1, "appid": API_KEY, "units": units}
    city1_results = requests.get(API_URL, params=city1_params).json()
    print(f"WHAT IS HAPPENING?: {city1_results}")
    sunset1 = datetime.fromtimestamp(city1_results['sys']['sunset'])
    date = datetime.now()
    city1_results_json = {
        'date': date.strftime("%D %H:%M:%S"),
        'city': city1_results['name'],
        'description': city1_results['weather'][0]['description'],
        'temp': city1_results['main']['temp'],
        'humidity': city1_results['main']['humidity'],
        'wind_speed': city1_results['wind']['speed'],
        'sunrise': datetime.fromtimestamp(city1_results['sys']['sunrise']).strftime("%H:%M:%S"),
        'sunset': int(sunset1.strftime("%H")),
        'units_letter': get_letter_for_units(units)

    }

    city2_params = {"q": city2, "appid": API_KEY, "units": units}
    city2_results = requests.get(API_URL, params=city2_params).json()
    print(f"WHAT IS HAPPENING?: {city2_results}")
    sunset2 = datetime.fromtimestamp(city2_results['sys']['sunset'])
    city2_results_json = {
        'date': date.strftime("%D %H:%M:%S"),
        'city': city2_results['name'],
        'description': city2_results['weather'][0]['description'],
        'temp': city2_results['main']['temp'],
        'humidity': city2_results['main']['humidity'],
        'wind_speed': city2_results['wind']['speed'],
        'sunrise': datetime.fromtimestamp(city2_results['sys']['sunrise']).strftime("%H:%M:%S"),
        'sunset': int(sunset2.strftime("%H")),
        'units_letter': get_letter_for_units(units)

    }
    print(f'This should be the hours: {sunset2.strftime("%H")}')

    # TODO: Pass the information for both cities in the context. Make sure to
    # pass info for the temperature, humidity, wind speed, and sunset time!
    # HINT: It may be useful to create 2 new dictionaries, `city1_info` and 
    # `city2_info`, to organize the data.

    context = {
        "city1": city1_results_json,
        "city2": city2_results_json,

    }

    return render_template('comparison_results.html', **context)


if __name__ == '__main__':
    app.config['ENV'] = 'development'
    app.run(debug=True)
