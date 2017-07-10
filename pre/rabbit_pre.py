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
import datetime

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
        q = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
        if 'False' == kind[1]:
            if not q.app_switch:
                SW = False
                channel.close()
                connection.close()
                print('##### end app : ' + str(rabbit_app_id))
        elif kind[1] == 'input':
            # todo
            if True:
                # app_model save
                if log_kind == '센서 온도':
                    sensor = int(kind[2].split('/')[0])
                    q.app_input_detail = "[{'icon': 'sun icon', 'value': '온도 : " + str(
                        sensor) + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + kind[2].split('/')[1] + "%'}]"
                elif log_kind == '센서 습도':
                    sensor = int(kind[2].split('/')[1])
                    q.app_input_detail = "[{'icon': 'sun icon', 'value': '온도 : " + \
                                         kind[2].split('/')[0] + "°C'}, {'icon': 'theme icon', 'value': '습도 : " + str(
                        sensor) + "%'}]"
                elif log_kind == '조도':
                    sensor = int(kind[2])
                    q.app_input_detail = "[{'icon': 'sun icon', 'value': '조도 : " + str(sensor) + "lux'}]"
                elif log_kind == '사람':
                    sensor = int(kind[2])
                    if sensor:
                        q.app_input_detail = "[{'icon': 'add user icon', 'value': '사람" + '' + " 인식'}]"
                    else:
                        q.app_input_detail = "[{'icon': 'add user icon', 'value': '사람" + '' + " 없음'}]"
                elif log_kind == '박수':
                    sensor = int(kind[2])
                    q.app_input_detail = "[{'icon': 'sign language icon', 'value': '횟수 : " + str(sensor) + "번'}]"
                elif log_kind == '버튼 눌림':
                    sensor = int(kind[2])
                    q.app_input_detail = "[{'icon': 'hand pointer icon', 'value': '횟수 : " + str(sensor) + "번'}]"
                else:
                    sensor = int(kind[2])
                q = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
                input_val = sensor

                # log
                in_node = q.in_node
                in_sensor = q.in_sensor
                # content = 'App ' + str(rabbit_app_id) + ' : Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                #           log_kind + ' ' + str(kind[2]) + ' 감지'
                if log_kind == '센서 온도':
                    temp1 = int(kind[2].split('/')[0])
                    temp2 = int(kind[2].split('/')[1])
                    temp = '온도:' + str(temp1) + '°C, 습도:' + str(temp2) + '%'
                    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + str(temp) + ' 감지'
                elif log_kind == '센서 습도':
                    temp1 = int(kind[2].split('/')[0])
                    temp2 = int(kind[2].split('/')[1])
                    temp = '온도:' + str(temp1) + '°C, 습도:' + str(temp2) + '%'
                    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + str(temp) + ' 감지'
                elif log_kind == '조도':
                    sensor = int(kind[2])
                    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                              '조도' + ' ' + str(sensor) + 'lux 감지'
                elif log_kind == '사람':
                    sensor = int(kind[2])
                    if sensor:
                        content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                                  '사람' + ' ' + '인식'
                    else:
                        content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                                  '사람' + ' ' + '없음'
                elif log_kind == '박수':
                    sensor = int(kind[2])
                    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                              '박수' + ' ' + str(sensor) + '회 감지'
                elif log_kind == '버튼 눌림':
                    sensor = int(kind[2])
                    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                              '버튼 눌림' + ' ' + str(sensor) + '회 감지'
                else:
                    temp = int(kind[2])
                    content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에서 ' + \
                              log_kind + ' ' + str(temp) + ' 감지'
                print(content)
                item = AppLog(content, rabbit_app_id, str(in_node), str(in_sensor),
                              str(datetime.datetime.utcnow()).split('.')[0])
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

    channel.queue_declare(queue='app_' + str(rabbit_app_id))
    channel.basic_consume(callback, queue='app_' + str(rabbit_app_id), no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


pt = threading.Thread(target=rabbit)
pt.start()
