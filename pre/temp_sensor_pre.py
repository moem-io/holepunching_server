# temperatureFromSensor
from requests import get
import json
import time

sensor_first = True

def temperatureFromSensor():
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
    print('temp sensor: ', humi)
    return humi