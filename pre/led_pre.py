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

# led
def ledRun(input=90):
    print('led output', input)
    db = session.query(Sensors).all()
    # print(db)

    #todo 모터의 번호를 설정디비에서 가저옴
    #todo 3번 모터의 값이 입력값과 같은지 확인
    #todo 만약 같지 않으면 래빗엠큐로 보내고, 디비에 저장하든말든 함

    # rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='led_q')
    channel.basic_publish(exchange='',
                          routing_key='led_q',
                          body='1'+','+str(input))
    print("RABBITMQ, led queue, Send "+str(input))
    connection.close()
    #todo 같으면 아무것도 안함