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
channel.queue_declare(queue='app_2')
channel.basic_publish(exchange='', routing_key='app_2', body='2'+','+'input'+','+'2')
print("RABBITMQ, Send " + str('send'))

channel.close()
connection.close()


