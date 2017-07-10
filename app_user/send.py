from requests import get
import json
import time
import threading
import paho.mqtt.client as mqtt
import pika
import time
import json
from requests import post


connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='app_5')
channel.basic_publish(exchange='', routing_key='app_5', body='5'+','+'input'+','+'3')
print("RABBITMQ, Send " + str('send'))

channel.close()
connection.close()


