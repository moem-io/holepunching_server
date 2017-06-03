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
channel.queue_declare(queue='app_18')
channel.basic_publish(exchange='', routing_key='app_18', body='app_switch_toggle,')
print("RABBITMQ, Send " + str('hi'))
connection.close()
