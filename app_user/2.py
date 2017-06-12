#-*- coding: utf-8 -*-
# api_url = API_URL
api_url = 'http://127.0.0.1:5000/'
# checkButtonCount
def checkButtonCount():
    global input_sw
    global input_val
    while input_sw:
        continue
    input_sw = True
    return input_val

# motor_pre
import threading
import pika

# db
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.models.nodes import Nodes
from app.models.sensor import Sensors
from app import session


# motor
def motorRun(angle=90):
    global rabbit_app_id
    print('motor angle', angle)
    db = session.query(Sensors).all()
    # print(db)

    #todo 모터의 번호를 설정디비에서 가저옴
    #todo 3번 모터의 값이 입력값과 같은지 확인
    #todo 만약 같지 않으면 래빗엠큐로 보내고, 디비에 저장하든말든 함

    # rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='motor_q')
    channel.basic_publish(exchange='',
                          routing_key='motor_q',
                          body=str(rabbit_app_id)+','+str(angle)+',motor_q')
    print("RABBITMQ, motor queue, Send "+str(angle))
    connection.close()
    #todo 같으면 아무것도 안함

log_kind = "버튼 눌림"

rabbit_app_id = 2

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


print('ss')
while SW:
  if checkButtonCount() > 20:
    motorRun(0)
  else:
    motorRun(150)
