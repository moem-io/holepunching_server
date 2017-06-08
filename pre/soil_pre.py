# soil
from requests import get
import json
import time

sensor_first = True

def soilHumidity():
    global sensor_first
    temp = 0
    if sensor_first:
        sensor_first = False
    else:
        time.sleep(10)

    # todo
    node_id = 1
    seoor_id = 1
    soil_data = 24
    print('soil humi : ', soil_data)
    return soil_data