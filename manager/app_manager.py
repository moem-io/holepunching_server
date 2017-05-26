import pika
import os
import sys
import subprocess

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='app_q')
# channel.queue_declare(queue='app_q') # 한개만 됨

def callback(ch, method, properties, body):
    print(" RABBITMQ app_manager, Received %r" % body)

    kind = body.decode().split(',')
    print(kind)
    if kind[0] == 'app_start':
        # os.system('ls')
        # result = subprocess.check_output('../app_user/python '+kind[1]+'.py')
        # result = subprocess.check_output('ls')
        # result = subprocess.call('../app_user/python '+kind[1]+'.py')
        # print('os.pardir()', os.pardir)
        os.system('cd .. && source .env && python app_user/'+kind[1]+'.py')
        # os.system('source 1.sh')


channel.basic_consume(callback, queue='app_q', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()