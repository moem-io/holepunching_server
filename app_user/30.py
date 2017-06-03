#-*- coding: utf-8 -*-

# weather_pre
from requests import get
import json
import time

# 기상청 온도는 1시간 단위로 변함(30~40분 사이에 뜸)
# 대기 타다가 정각에 가져오는걸로 만들자
weatherFirst = True

def temperatureFromSky():
    global weatherFirst
    temp = 0
    if weatherFirst:
        weatherFirst = False
    else:
        time.sleep(10)
    res = get('https://api.moem.io/outside/weather')
    js = json.loads(res.text)
    for i in js['json_list']:
        if i['category'] == 'T1H':
            # print('temp:'+str(i['obsrValue']))
            temp = i['obsrValue']
    print('temperature : ', temp)
    return temp



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
                          body='1'+','+str(angle))
    print("RABBITMQ, motor queue, Send "+str(angle))
    connection.close()
    #todo 같으면 아무것도 안함

rabbit_app_id = 30

# rabbit pre
from app.models.app_model import AppModel
import pika
import threading
from app import session

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

sw = True
def callback(ch, method, properties, body):
    global sw
    global connection
    global channel
    global rabbit_app_id

    kind = body.decode().split(',')
    print('kind[0]', kind[0])
    print('kind[1]', kind[1])
    print('rabbit', str(rabbit_app_id))

    if kind[0] == str(rabbit_app_id):
        query = session.query(AppModel).filter_by(id=kind[0]).first()
        print('query30', query.app_switch)
        if 'False' == kind[1]:
            sw = False
            channel.close()
            connection.close()
            print('get'+str(rabbit_app_id))


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


print('기상청 온도로 문 닫기')
while sw:
  if temperatureFromSky() < 18:
    motorRun(0)
  else:
    motorRun(180)
