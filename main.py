import requests
from twilio.rest import Client
from config import credentials

account_sid = credentials['account_sid']
auth_token = credentials['auth_token']

api_key=credentials['OWM_API_KEY']
OWM_endpoint = 'https://api.openweathermap.org/data/2.5/onecall'
weather_params = {
    'lat':43.653225,
    'lon':-79.383186,
    'appid':api_key,
    'exclude':'current,minutely,daily',
    'units':'metric'
}
response = requests.get(OWM_endpoint,params=weather_params)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data['hourly'][:12]
will_rain = False

for hour in weather_slice:
    condition_code = hour['weather'][0]['id']
    if int(condition_code)<700:
        will_rain=True

if will_rain:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body="It is going to rain today. Carry your umbrella",
        from_=credentials['from'],
        to=credentials['user_number']
    )
    print(message.status)
else:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
        body=f"It is going to be cloudy today⛅ in {weather_data['timezone']} with a temperature of {round((weather_data['hourly'][0]['temp']))} degree Celsius ~ Daivik😉.",
        from_=credentials['from'],
        to=credentials['user_number']
    )
    print(message.status)

