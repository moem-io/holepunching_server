# motor_pre
import threading
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello')

channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print(" [x] Sent 'Hello World!'")
connection.close()


motor_end = False
def get_motor(second=10):

    threading.Timer(second, get_motor, [second]).start()
get_motor(1)

# db
from app.models.nodes import Nodes
from app.models.sensor import Sensors
from app import session

# motor
def motorRun(angle=90):
    print('motor angle', angle)
    db = session.query(Sensors).all()
    print(db)

    #todo 모터의 번호를 설정디비에서 가저옴
    #todo 3번 모터의 값이 입력값과 같은지 확인
    #todo 만약 같지 않으면 래빗엠큐로 보내고, 디비에 저장하든말든 함
    #todo 같으면 아무것도 안함