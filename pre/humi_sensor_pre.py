# humidityFromSensor
from requests import get
import json
import time

sensor_first = True

def humidityFromSensor():
    global sensor_first
    temp = 0
    if sensor_first:
        sensor_first = False
    else:
        time.sleep(10)

    # todo
    node_id = 1
    seoor_id = 1
    humi = 24
    print('humi sensor: ', humi)
    return humi