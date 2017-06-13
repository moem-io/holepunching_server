#-*- coding: utf-8 -*-

# checkButtonCount
def checkButtonCount():
    global input_sw
    global input_val
    while input_sw:
        continue
    input_sw = True
    return input_val

# ledRun
import threading
import pika

# db
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.models.nodes import Nodes
from app.models.sensor import Sensors
from app import session
from app.models.app_setting import AppSetting
from app.models.app_model import AppModel


def ledRun(input=90):
    print('led output', input)
    global rabbit_app_id

    rgb = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
    if not rgb == input:
        sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='led_q')
        channel.basic_publish(exchange='',
                              routing_key='led_q',
                              body=str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + str(input))
        print("RABBITMQ, led queue, Send " + str(input))
        connection.close()

log_kind = "버튼 눌림"

rabbit_app_id = 8

# rabbit pre
from app.models.app_model import AppModel
import pika
import threading
from app import session
from app.models.app_log import AppLog
from app.models.app_setting import AppSetting
from requests import post
from config import *
import json
from manager.make_app import AlchemyEncoder

api_url = API_URL

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

SW = True
input_sw = True
input_val = None

def callback(ch, method, properties, body):
    global SW
    global connection
    global channel
    global rabbit_app_id
    global input_sw
    global input_val
    global log_kind
    global api_url

    kind = body.decode().split(',')
    if kind[0] == str(rabbit_app_id):
        # query = session.query(AppModel).filter_by(id=kind[0]).first()
        if 'False' == kind[1]:
            SW = False
            channel.close()
            connection.close()
            print('end app : '+str(rabbit_app_id))
        elif kind[1] == 'input':
            input_val = int(kind[2])
            q = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
            in_node = q.in_node
            in_sensor = q.in_sensor
            content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                      log_kind + ' ' + str(input_val) + ' 감지'
            item = AppLog(content, rabbit_app_id, str(in_node), str(in_sensor))
            session.add(item)
            session.commit()

            c = session.query(AppLog).order_by('id').all()
            res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))
            print(res)
            input_sw = False


def rabbit():
    global connection
    global channel
    global rabbit_app_id

    channel.queue_declare(queue='app_'+str(rabbit_app_id))
    channel.basic_consume(callback, queue='app_'+str(rabbit_app_id), no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

pt = threading.Thread(target=rabbit)
pt.start()


print('기상청 온도로 모터 실행')
while SW:
  if checkButtonCount() == 1:
    ledRun(151515)
  else:
    ledRun(151515)
