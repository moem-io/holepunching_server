# temperatureFromSensor
from requests import get
import json
import time
from app import session
from app.models.app_setting import AppSetting
from app.models.app_log import AppLog
import datetime
from requests import post
from manager.make_app import AlchemyEncoder
import pika

sensor_first = True


def temperatureFromSensor():
    global sensor_first
    global rabbit_app_id
    global input_sw
    global input_val
    if sensor_first:
        sensor_first = False
    else:
        time.sleep(10)

    sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()

    # rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='sensor_q')
    channel.basic_publish(exchange='',
                          routing_key='sensor_q',
                          body=str(sett.in_node) + ',' + str(sett.in_sensor) + ',' + str(rabbit_app_id) + ',' + 'temp')
    connection.close()

    while input_sw:
        continue
    input_sw = True
    return input_val
