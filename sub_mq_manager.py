import paho.mqtt.client as mqtt
import pika
import time

def getAppModi(app_origin):

    app = app_origin.split(',')
    app_title = app[0]
    app_contnet = app[1]
    # print('app_title', app_title)
    # print('app_contnet', app_contnet)


    # 만약 특정 변수가 발견되면 그 변수에 맞는거 가져옴
    pre = '#-*- coding: utf-8 -*-\n'

    # print(app_origin.count('temp')
    if app_origin.count('temperatureFromSky()'):
        pre += open('pre/weather_pre.py', 'r').read() + '\n\n'
    if app_origin.count('motorRun'):
        pre += open('pre/motor_pre.py', 'r').read() + '\n\n'

    # 앱 변형
    modi = pre + '\n' + app_contnet

    # 완료된 앱
    f_modi = open('./app_user/'+app_title+'.py', 'w')
    f_modi.write(modi)
    f_modi.close()

    return app_title


def on_connect(client, userdata, rc):
    print('connected with result'+str(rc))
    client.subscribe('control/motor/00001214')
    client.subscribe('app/upload')
    client.subscribe('app/upload/00001214')

def on_message(client, userdata, msg):
    print("MQTT, Topic: ", msg.topic + ', Message: ' + str(msg.payload))

    if msg.topic == 'app/upload/00001214':
        app_title = getAppModi(app_origin=msg.payload.decode())

        time.sleep(3)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='app_q')
        channel.basic_publish(exchange='', routing_key='app_q', body='app_start,'+app_title)
        print("RABBITMQ,", 'app_start,'+app_title)
        connection.close()

    elif msg.topic == 'control/motor/00001214':
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='motor_q')
        channel.basic_publish(exchange='', routing_key='motor_q', body=msg.payload.decode())
        print("RABBITMQ, Send "+str(msg.payload))
        connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('13.124.19.161', 1883, 60)
client.loop_forever()