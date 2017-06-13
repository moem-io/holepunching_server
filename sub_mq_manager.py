import paho.mqtt.client as mqtt
import pika
import time
from app.models.app_model import AppModel
from app.models.app_setting import AppSetting
from app import session
import json
from requests import post
from sqlalchemy.ext.serializer import loads, dumps
from config import *
from manager.make_app import getAppModi
from manager.make_app import AlchemyEncoder

api_url = API_URL
# api_url = 'http://127.0.0.1:5000/'

def on_connect(client, userdata, rc):
    print('connected with result' + str(rc))
    client.subscribe('control/app/00001214')
    client.subscribe('control/motor/00001214')
    client.subscribe('control/led/00001214')
    client.subscribe('app/upload')
    client.subscribe('app/upload/00001214')
    client.subscribe('app/switch_toggle/00001214')
    client.subscribe('app/output/00001214')
    client.subscribe('app/setting/00001214')


def on_message(client, userdata, msg):
    print("MQTT, Topic: ", msg.topic + ', Message: ' + str(msg.payload))

    if msg.topic == 'control/app/00001214':
        # time.sleep(1) 이게 느리면 웹에 반영이 느림
        session.commit()
        c = session.query(AppModel).order_by('id').all()

        # c = AppModel.query.all()
        for i in c:
            print('c', i.app_switch)
        # query = session.query(AppModel).filter_by(id=18).first()
        # query = session.query(AppModel).order_by(AppModel.id.desc()).first()
        # print('qq,c', query.app_switch)

        # session.commit()

        res = post(api_url + 'app/save', data=json.dumps(c, cls=AlchemyEncoder))
        print(res)

        # res = post('http://127.0.0.1:5000/' + 'app/save', data=json.dumps(c, cls=AlchemyEncoder))
        # print('res', res)

        # for i in json.loads(json.dumps(c, cls=AlchemyEncoder)):
        #     print('data', i['app_name'])

    elif msg.topic == 'app/upload/00001214':
        app_title = getAppModi(app_origin=msg.payload.decode())
        print('upload completed')
        # time.sleep(3)
        #
        # connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        # channel = connection.channel()
        # channel.queue_declare(queue='app_q')
        # channel.basic_publish(exchange='', routing_key='app_q', body='app_upload,' + app_title)
        # print("RABBITMQ,", 'app_upload,' + app_title)
        # connection.close()

    elif msg.topic == 'control/motor/00001214':
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='motor_q')
        channel.basic_publish(exchange='', routing_key='motor_q', body=msg.payload.decode())
        print("RABBITMQ, Send " + str(msg.payload))
        connection.close()

    elif msg.topic == 'control/led/00001214':
        data = msg.payload.decode().split(',')
        app_id = data[0]
        query = session.query(AppModel).filter_by(app_id=app_id).first()
        led_rgb = data[1]
        query.app_output_detail = led_rgb

        #
        sett = session.query(AppSetting).filter_by(app_id=app_id).first()

        session.commit()

        res = post(api_url+'app/save/one', data=json.dumps(query, cls=AlchemyEncoder))

        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='led_q')
        channel.basic_publish(exchange='',
                              routing_key='led_q',
                              body=str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + str(led_rgb))
        print("RABBITMQ, Send " + str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + str(led_rgb))
        connection.close()

    elif msg.topic == 'app/switch_toggle/00001214':
        app_id = msg.payload.decode()
        query = session.query(AppModel).filter_by(app_id=app_id).first()

        # print('query1', (query.app_switch))
        if query:
            if query.app_switch:
                query.app_switch = False
            else:
                query.app_switch = True
            session.commit()
            query = session.query(AppModel).filter_by(app_id=app_id).first()
            print('swit', query.app_switch)

            # c = session.query(AppModel).order_by('id').all()
            # res = post(api_url + 'app/save', data=json.dumps(c, cls=AlchemyEncoder))
            # print(res)

            res = post(api_url + 'app/save/one', data=json.dumps(query, cls=AlchemyEncoder))
            # print(res)

            # rabbit
            connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            channel = connection.channel()
            channel.queue_declare(queue='app_manage')
            channel.basic_publish(exchange='', routing_key='app_manage',
                                  body='app_switch_toggle,' + msg.payload.decode() + ',' + str(query.app_switch))
            # print("RABBITMQ, Send " + str(msg.payload))
            connection.close()

    elif msg.topic == 'app/output/00001214':
        data = msg.payload.decode().split(',')
        app_id = data[0]
        query = session.query(AppModel).filter_by(app_id=app_id).first()
        query.app_output_detail = data[1]
        session.commit()

        res = post(api_url + 'app/save/one', data=json.dumps(query, cls=AlchemyEncoder))

        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue=data[2])
        channel.basic_publish(exchange='', routing_key=data[2], body=msg.payload.decode())
        print("RABBITMQ, Send " + str(msg.payload))
        connection.close()

    elif msg.topic == 'app/setting/00001214':

        data = msg.payload.decode().split(',')
        app_id = data[0]

        session.query(AppSetting).filter_by(app_id=app_id).delete()
        session.add(AppSetting(app_id, data[1], data[2], data[3], data[4]))
        session.commit()


        # time.sleep(1) 얘는 프로세스 자체 멈추니까 웹에 반영도 느려져..안돼

        # print('query', (query.app_switch))
        # payload = dumps(query)
        # print('payload', payload)

        # print('json', json.dumps(c, cls=AlchemyEncoder))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('13.124.19.161', 1883, 60)
client.loop_forever()