import paho.mqtt.client as mqtt
import pika
import time
from app.models.app_model import AppModel
from app import session
import json
from requests import post
from sqlalchemy.ext.serializer import loads, dumps

# web_url = 'https://52.79.188.83/'
api_url = 'http://127.0.0.1:5000/'

from sqlalchemy.ext.declarative import DeclarativeMeta


class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)


def getAppModi(app_origin):
    # 가져온 정보
    app = app_origin.split(',')
    app_title = app[0]
    app_sub = app[1]
    app_content = app[2]
    # print('app_title', app_title)
    # print('app_contnet', app_contnet)

    # 앱 제작 중
    app_switch = False

    # 만약 특정 변수가 발견되면 그 변수에 맞는거 가져옴
    pre = '#-*- coding: utf-8 -*-\n\n'

    app_input = ''
    input_detail = "[{'icon': 'hand rock icon', 'value': '두 번'}, {'icon': 'bullseye icon', 'value': '세기 : 45%'}]"
    output = ''
    output_meta = ''
    output_detail = False

    # print(app_origin.count('temp')
    if app_origin.count('temperatureFromSky()'):
        pre += open('pre/weather_pre.py', 'r').read() + '\n\n'
        app_input += '기상청 온도 및 습도'
        input_detail = "[{'icon': 'sun icon', 'value': '24°C'}, {'icon': 'theme icon', 'value': '세기 : 15%'}]"
        print('input', input)
    else:
        input_detail = "[{'icon': 'angle double down icon', 'value': '24 Pa'}]"
        input_detail = "[{'icon': 'sun icon', 'value': '24°C'}, {'icon': 'theme icon', 'value': '세기 : 15%'}]"
        input_detail = "[{'icon': 'hand rock icon', 'value': '두 번'}, {'icon': 'bullseye icon', 'value': '세기 : 45%'}]"

    if app_origin.count('motorRun'):
        pre += open('pre/motor_pre.py', 'r').read() + '\n\n'
        output += '서보 모터'


    # add db
    db_app = session.query(AppModel).filter_by(app_name=app_title).first()
    if db_app:
        session.query(AppModel).filter_by(app_name=app_title).delete()
    session.add(AppModel(app_title, app_sub, app_switch, app_input, input_detail, output, output_detail))
    session.commit()

    query = session.query(AppModel).order_by(AppModel.id.desc()).first()
    print('query.id', query.id)

    # final pre
    pre += 'rabbit_app_id = ' + str(query.id) + '\n\n'
    pre += open('pre/rabbit_pre.py', 'r').read() + '\n\n'

    # 앱 변형
    modi = pre + '\n' + app_content

    # 완료된 앱
    f_modi = open('./app_user/' + str(query.id) + '.py', 'w')
    f_modi.write(modi)
    f_modi.close()

    query = session.query(AppModel).all()
    print('query', (query))
    c = query
    res = post(api_url + 'app/save', data=json.dumps(c, cls=AlchemyEncoder))

    session.close()
    return app_title


def on_connect(client, userdata, rc):
    print('connected with result' + str(rc))
    client.subscribe('control/motor/00001214')
    client.subscribe('control/app/00001214')
    client.subscribe('app/upload')
    client.subscribe('app/upload/00001214')
    client.subscribe('app/switch_toggle/00001214')


def on_message(client, userdata, msg):
    print("MQTT, Topic: ", msg.topic + ', Message: ' + str(msg.payload))

    if msg.topic == 'control/app/00001214':
        # time.sleep(1) 이게 느리면 웹에 반영이 느림

        c = session.query(AppModel).order_by('id').all()
        # c = AppModel.query.all()
        for i in c:
            print('c', i.app_switch)


        # query = session.query(AppModel).filter_by(id=18).first()
        # query = session.query(AppModel).order_by(AppModel.id.desc()).first()
        # print('qq,c', query.app_switch)

        # session.commit()
        res = post(api_url + 'app/save', data=json.dumps(c, cls=AlchemyEncoder))
        # print('res', res)

        for i in json.loads(json.dumps(c, cls=AlchemyEncoder)):
            print('data', i['app_name'])

    elif msg.topic == 'app/upload/00001214':
        app_title = getAppModi(app_origin=msg.payload.decode())

        time.sleep(3)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='app_q')
        channel.basic_publish(exchange='', routing_key='app_q', body='app_upload,' + app_title)
        print("RABBITMQ,", 'app_upload,' + app_title)
        connection.close()

    elif msg.topic == 'control/motor/00001214':
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='motor_q')
        channel.basic_publish(exchange='', routing_key='motor_q', body=msg.payload.decode())
        print("RABBITMQ, Send " + str(msg.payload))
        connection.close()

    elif msg.topic == 'app/switch_toggle/00001214':
        id = msg.payload.decode()
        query = session.query(AppModel).filter_by(id=id).first()

        print('query1', (query.app_switch))

        if query.app_switch:
            query.app_switch = False
        else:
            query.app_switch = True
        session.commit()

        # time.sleep(1) 얘는 프로세스 자체 멈추니까 웹에 반영도 느려져..안돼

        # print('query', (query.app_switch))
        # payload = dumps(query)
        # print('payload', payload)

        # print('json', json.dumps(c, cls=AlchemyEncoder))

        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='app_q')
        channel.basic_publish(exchange='', routing_key='app_q', body='app_switch_toggle,' + msg.payload.decode()+','+str(query.app_switch))
        print("RABBITMQ, Send " + str(msg.payload))
        connection.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('13.124.19.161', 1883, 60)
client.loop_forever()
