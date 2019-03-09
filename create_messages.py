import json
import urllib
import requests
import cognitive_face as CF
from constants import simulator_ip
from utils import get_avalible_signal_names, get_signal_data
import http.client, urllib.request, urllib.parse, urllib.error, base64




def weather_message():
    from constants import weather_key
    lat = get_signal_data(simulator_ip, 'NP_LatDegree')
    lon = get_signal_data(simulator_ip, 'NP_LongDegree')
    w = requests.get(
    'http://api.openweathermap.org/data/2.5/weather?lat=' + str(lat['value']) + '&lon=' + str(lon['value']) + '&APPID={}'.format(weather_key)).json()
    s = "This is a " + w['weather'][0]['description'] + " outside. " + '\n'
    s += "The temperature is " + str(int(w['main']['temp']) - 273) + " Celsius." + '\n'
    s += "The roads are slippery." + "\n"
    s += "The recommended speed is 60 km per hour." + "\n"
    s += "Don't forget to turn on your low-beam headlights. " + '\n'
    return s

def emotion_message(pwd):
    from constants import emotions_key
    KEY = emotions_key  # Replace with a valid Subscription Key here.
    CF.Key.set(KEY)

    BASE_URL = 'https://eastus.api.cognitive.microsoft.com/face/v1.0'  # Replace with your regional Base URL
    CF.BaseUrl.set(BASE_URL)
    params = urllib.parse.urlencode({
        # Request parameters
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': '{}'.format('emotion'),
    })
    headers = {
        # Request headers
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '{}'.format(KEY),
    }
    data = open(pwd, 'rb').read()
    try:
        conn = http.client.HTTPSConnection('eastus.api.cognitive.microsoft.com')
        conn.request("POST", "/face/v1.0/detect?%s" % params, body=data, headers=headers)
        response = conn.getresponse()
        data = response.read()
        stats =  json.loads(data)[0]['faceAttributes']['emotion']
        conn.close()
        return (max(stats, key = stats.get))
    except Exception as e:
        return 'error'