import paho.mqtt.client as mqtt
import pika

def on_connect(client, userdata, rc):
    print('connected with result'+str(rc))
    client.subscribe('hello/world')

def on_message(client, userdata, msg):
    print("Topic: ", msg.topic + '\nMessage: ' + str(msg.payload))

    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='hello')

    channel.basic_publish(exchange='',
                          routing_key='hello',
                          body='Hello World!')
    print(" [x] Sent 'Hello World!'")
    connection.close()


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# client.connect('test.mosquitto.org', 1883, 60)
client.connect('13.124.19.161', 1883, 60)

client.loop_forever()