import json
import urllib
import requests
import cognitive_face as CF
from constants import simulator_ip
from utils import get_avalible_signal_names, get_signal_data
import http.client, urllib.request, urllib.parse, urllib.error, base64
import gmplot



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


def check_gas():
    gas_percent = get_signal_data(simulator_ip, 'KBI_Tankfuellstand_Prozent')['value']
    if (gas_percent < 6):
        return "Caution! Critical gas level" + str(gas_percent) + "left"
    if (gas_percent < 20):
        return "Low gas level." + str(gas_percent) + "left"

def check_belt():
    v_signal = get_signal_data(simulator_ip, 'ESP_v_Signal')
    v = v_signal['value']
    belt_signal = get_signal_data(simulator_ip, 'AB_Gurtschloss_FA')
    belt = belt_signal['value']
    if (v > 0 and belt == 2):
        s = "The driver seat belt is not fastened."
        return s

def check_blinkers():
    angle = get_signal_data(simulator_ip, 'LWI_Lenkradwinkel')['value']
    left_blinker = get_signal_data(simulator_ip, 'BH_Blinker_li')['value']
    right_blinker = get_signal_data(simulator_ip, 'BH_Blinker_re')['value']
    direction = get_signal_data(simulator_ip, 'LWI_VZ_Lenkradwinkel')['value']
    cur_speed = get_signal_data(simulator_ip, 'ESP_v_Signal')['value']
    if (cur_speed > 1 and angle > 90):
        if (direction):
            if (not left_blinker and right_blinker):
                return "You turned on the wrong blinker."
            if (not left_blinker and not right_blinker):
                return "You forgot turn on left blinker."
        else:
            if (left_blinker and not right_blinker):
                return "You turned on the wrong blinker."
            if (not left_blinker and not right_blinker):
                return "You forgot turn on right blinker."

def check_lights():
    from datetime import datetime
    import pytz
    part_of_day = 'night'
    tz_ZR = pytz.timezone('Europe/Zurich')
    datetime_ZR = datetime.now(tz_ZR)
    a = ()
    a = datetime_ZR.strftime("%H%M%S")
    h, m, s, = (a[0]+a[1]), (a[2]+a[3]), (a[4]+a[5])
    if (int(h) < 18 and int(h) > 6):
        part_of_day = 'day'
    dipped = get_signal_data(simulator_ip, "LV_Abblendlicht_Anzeige")
    high = get_signal_data(simulator_ip, "BH_Fernlicht")
    if (part_of_day == 'day'):
        if (high):
            return "Turn off high beam"
    if (not dipped):
        return "Put dipped beam on"
    #     Dipped beam должен быть включен всегда
    #     High beam выключен днем всегда

def get_coordinates():
    lat = get_signal_data(simulator_ip, 'NP_LatDegree')['value']
    lon = get_signal_data(simulator_ip, 'NP_LongDegree')['value']
    # print(lat, lon)
    return lat, lon

def check_speed():
    cur_speed = get_signal_data(simulator_ip, 'ESP_v_Signal')['value']
    limit_speed = 30
    if (cur_speed > limit_speed):
        return "You have exceeded the speed limit."



latitude, longtitude = get_coordinates()
if (latitude and longtitude):
    latitude_list = []
    longitude_list = []
    latitude_list.append(latitude)
    longitude_list.append(longtitude)
    gmap3 = gmplot.GoogleMapPlotter(latitude_list[0], longitude_list[0], 13)
def plot_points():
    if (len(latitude_list) > 0 and len(longitude_list) > 0):
        latitude, longtitude = get_coordinates()
        if(len(latitude_list) > 100):
            longitude_list.clear()
            longitude_list.clear()
        latitude_list.append(latitude)
        longitude_list.append(longtitude)
        if (len(latitude_list) % 10 == 0):
            # print(latitude_list)
            # print(longitude_list)

            # scatter method of map object
            # scatter points on the google map
            gmap3.scatter(latitude_list, longitude_list, '# FF0000',
                          size=5, marker=False)

            # Plot method Draw a line in
            # between given coordinates
            # gmap3.plot(latitude_list, longitude_list,
            #            'cornflowerblue', edge_width=10)

            gmap3.draw("templates/map.html")
