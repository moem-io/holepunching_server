import paho.mqtt.client as mqtt
import pika

def on_connect(client, userdata, rc):
    print('connected with result'+str(rc))
    client.subscribe('hello/world')

def on_message(client, userdata, msg):
    print("MQTT, Topic: ", msg.topic + 'Message: ' + str(msg.payload))

    # rabbit
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='hello')
    channel.basic_publish(exchange='', routing_key='hello', body=str(msg.payload))
    print("RABBITMQ, Send "+str(msg.payload))
    connection.close()

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect('13.124.19.161', 1883, 60)
client.loop_forever()