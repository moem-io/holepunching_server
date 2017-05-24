import paho.mqtt.client as mqtt
import pika

def on_connect(client, userdata, rc):
    print('connected with result'+str(rc))
    client.subscribe('control/motor')
    client.subscribe('app/upload')

def on_message(client, userdata, msg):
    print("MQTT, Topic: ", msg.topic + ', Message: ' + str(msg.payload))

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