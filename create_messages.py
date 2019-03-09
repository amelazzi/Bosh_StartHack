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
    s = "This is a "
    s += w['weather'][0]['description']
    s += " today. " + '\n'
    if (w['weather'][0]['main'] == 'Rain'):
        s += "First of all, turn on your low-beam headlights. " + '\n'
        s += "Be careful. Heavy rainfall can reduce visibility to zero. Pull over and wait for the rain to subside, or until visibility is restored."
    if (w['weather'][0]['main'] == 'Snow'):
        s += "Keep the windows and windshield clear." + '\n'
        s += "Obtain maximum visibility by turning on low-beam headlights and windshield wipers." + '\n'
        s += "Drive slowly and stay farther behind the vehicle ahead. Slow to a crawl on ice. Slow down as you approach curves and intersections." + '\n'
        s += "Avoid fast turns." + '\n'
        s += "Avoid quick stops." + '\n'
        s += "Shift to low gear before going down a steep hill, but do not downshift at too fast a speed." + '\n'
    return s
