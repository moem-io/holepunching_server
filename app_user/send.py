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
channel.queue_declare(queue='app_6')
channel.basic_publish(exchange='', routing_key='app_6', body='6'+','+'input'+','+'0')
print("RABBITMQ, Send " + str('send'))
connection.close()


