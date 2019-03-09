import json
import urllib
import requests
from constants import simulator_ip
from utils import get_avalible_signal_names, get_signal_data





def weather_message():
    lat = get_signal_data(simulator_ip, 'NP_LatDegree')
    lon = get_signal_data(simulator_ip, 'NP_LongDegree')
    w = requests.get(
    'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat['value']) + '&lon=' + str(lon['value']) + '&APPID=a7c0bfead821b64b6866e867d07a02eb').json()
    s = "This is a " + w['weather'][0]['description'] + " outside. " + '\n'
    s += "The temperature is " + str(int(w['main']['temp']) - 273) + " Celsius." + '\n'
    s += "The roads are slippery." + "\n"
    s += "The recommended speed is 60 km per hour." + "\n"
    s += "Don't forget to turn on your low-beam headlights. " + '\n'
    return s

print(weather_message())