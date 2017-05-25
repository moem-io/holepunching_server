import paho.mqtt.client as mqtt
import pika
import time

def getAppModi(app_origin):
    # 만약 특정 변수가 발견되면 그 변수에 맞는거 가져옴
    pre = ''
    # print(app_origin.count('temp')
    if app_origin.count('temperatureFromSky()'):
        pre += open('weather_pre.py', 'r').read() + '\n\n'
    if app_origin.count('motorRun'):
        pre += open('motor_pre.py', 'r').read() + '\n\n'

    # 앱 변형
    modi = app_origin
    if pre:
        modi = pre + '\n' + app_origin

    # 완료된 앱
    f_modi = open('./app_user/test_1214.py', 'w')
    f_modi.write(modi)
    f_modi.close()


def on_connect(client, userdata, rc):
    print('connected with result'+str(rc))
    client.subscribe('control/motor')
    client.subscribe('app/upload')
    client.subscribe('app/upload/00001214')

def on_message(client, userdata, msg):
    print("MQTT, Topic: ", msg.topic + ', Message: ' + str(msg.payload))

    if msg.topic == 'app/upload/00001214':
        getAppModi(app_origin=msg.payload.decode())

        time.sleep(3)

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='app_q')
        channel.basic_publish(exchange='', routing_key='app_q', body=msg.topic+', app_start')
        print("RABBITMQ, Send app_q")
        connection.close()

    elif msg.topic == 'control/motor':
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='motor_q')
        channel.basic_publish(exchange='', routing_key='motor_q', body=str(msg.payload))
        print("RABBITMQ, Send "+str(msg.payload))
        connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('13.124.19.161', 1883, 60)
client.loop_forever()


