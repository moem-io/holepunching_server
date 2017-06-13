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
        session.commit()
        if 'False' == kind[1]:
            q = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
            if not q.app_switch:
                SW = False
                channel.close()
                connection.close()
                print('##### end app : '+str(rabbit_app_id))
        elif kind[1] == 'input':
            input_val = int(kind[2])

            # log
            q = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
            in_node = q.in_node
            in_sensor = q.in_sensor
            content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                      log_kind + ' ' + str(input_val) + ' 감지'
            print(content)
            item = AppLog(content, rabbit_app_id, str(in_node), str(in_sensor))
            session.add(item)
            session.commit()
            c = session.query(AppLog).order_by('id').all()
            res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))
            # print(res)
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