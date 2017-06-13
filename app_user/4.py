#-*- coding: utf-8 -*-

# temperatureFromSky
from requests import get
import json
import time

# 기상청 온도는 1시간 단위로 변함(30~40분 사이에 뜸)
# 대기 타다가 정각에 가져오는걸로 만들자
weatherFirst = True

def temperatureFromSky():
    global weatherFirst
    global SW
    temp = 0
    if weatherFirst:
        weatherFirst = False
    else:
        time.sleep(10)
    if not SW:
        return 0
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'T1H':
            # print('temp:'+str(i['obsrValue']))
            temp = i['obsrValue']
    print('temperature : ', temp)
    return temp

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
    global rabbit_app_id
    global SW
    if not SW:
        return 0

    # todo led 비교 후 내보내기
    # rgb = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
    # rgb_in = rgb.app_output_detail
    # if not rgb == input:
    if True:
        sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='led_q')
        channel.basic_publish(exchange='',
                              routing_key='led_q',
                              body=str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + str(input))
        print('led output', input)
        print('')
        # print("RABBITMQ, led queue, Send " + str(input))
        connection.close()


log_kind = "온도"

rabbit_app_id = 4

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
            session.commit()
            q = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
            if not q.app_switch:
                SW = False
                channel.close()
                connection.close()
                print('##### end app : '+str(rabbit_app_id))
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


print('기상청 온도로 LED 제어')
while SW:
  if temperatureFromSky() > 18:
    ledRun(151515)
  else:
    ledRun(151515)
