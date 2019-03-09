import json
import urllib
from flask import request
from constants import simulator_ip

def get_avalible_signal_names(ip):
    d = json.loads(urllib.request.urlopen("http://" + ip+'/list').read().decode("utf-8"))
    return d['gateway']['signals']

def get_signal_data(ip, signal_name):
    d = json.loads(urllib.request.urlopen("http://" + ip+'/signal/' + signal_name + '/value').read().decode("utf-8"))
    return d['measurement']


print(get_avalible_signal_names(simulator_ip))
print(get_signal_data(simulator_ip, 'AB_Gurtschloss_BF'))