# -*- coding: utf-8 -*-

import pika
import os
import sys
import subprocess
from app import session
from app.models.app_model import AppModel
import pexpect
import threading
import time

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='app_q')


# channel.queue_declare(queue='app_q') # 한개만 됨

def spawn_app(i):
    os.system('cd .. && source .env && python app_user/' + i + '.py')



def callback(ch, method, properties, body):
    print("\nRABBITMQ app_manager, Received %r" % body)

    kind = body.decode().split(',')
    print(kind)
    if kind[0] == 'app_upload':
        os.system('ls')
        # result = subprocess.check_output('../app_user/python '+kind[1]+'.py')
        # result = subprocess.check_output('ls')
        # result = subprocess.call('../app_user/python '+kind[1]+'.py')
        # print('os.pardir()', os.pardir)
        # os.system('cd .. && source .env && python app_user/' + kind[1] + '.py')
        # os.system('source 1.sh')

        # proc = subprocess.Popen(
        #     ['echo', 'hellow'],
        #     stdout=subprocess.PIPE
        # )
        # out, err = proc.communicate()
        # print(out.decode())

    elif kind[0] == 'app_switch_toggle':
        print('kind[1]', kind[1])
        query = session.query(AppModel).filter_by(id=kind[1]).first() # 얘 반응이 느리다..왜지?
        print('query2', query.app_switch)
        print('swt', kind[2])

        if 'False' == kind[2]:
            conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            ch = conn.channel()
            ch.queue_declare(queue='app_'+(kind[1]))
            ch.basic_publish(exchange='', routing_key='app_'+(kind[1]), body=(kind[1])+','+(kind[2]))
            print("RABBITMQ, Send " + str(kind[1]))
            conn.close()
            # ch.close() 이거 하면 안됨
        else:

            pt = threading.Thread(target=spawn_app, args=(kind[1],))
            pt.start()

        # session.commit()
        # query = session.query(AppModel).filter_by(id=kind[1]).first()
        # print('query3', query.app_switch)
        # session.close()


        # 됨
        # os.system('cd .. && source .env && python app_user/' + kind[1] + '.py')
        # pt = threading.Thread(target=spawn_app, args=(kind[1],))
        # pt.start()


        print('threading.activeCount()', threading.activeCount())
        print('threading.currentThread()', threading.currentThread())
        print('threading.enumerate()', threading.enumerate())
        # 실험


        # 안됨
        # child = pexpect.spawn('cd .. && source .env && python ../app_user/'+kind[1]+'.py')
        # child.expect('hee')

        # result = subprocess.call('date')
        # result = subprocess.call('cd .. && source .env && python ../app_user/'+kind[1]+'.py')
        # result = subprocess.call('cd ..')
        # result = subprocess.call('cd .. && source .env && python app_user/'+kind[1]+'.py')

        # p = subprocess.Popen(['cd ..', ''], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        # print(p.communicate())


        # child = pexpect.spawn('python ../app_user/'+kind[1]+'.py')
        # child = pexpect.spawn('cd ..')
        # child.interact()
        # ret = child.expect('print')
        # print('ret', ret)
        # print(child.before)

channel.basic_consume(callback, queue='app_q', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
