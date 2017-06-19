# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

import pika
import os
from multiprocessing import Process
from app.models.app_model import AppModel
from app.models.app_log import AppLog
from app import session
import datetime
from config import *
api_url = API_URL
from requests import post
from manager.make_app import AlchemyEncoder
import json

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='loq_q')

# channel.queue_declare(queue='app_q') # 한개만 됨

# def spawn_app(i):
#     os.system('cd .. && source .env && python app_user/' + i + '.py')

# class SpawnApp():
#     def __init__(self, app_id):
#         self.app_id = app_id
#
#     def run(self):
#         os.system('cd .. && source .env && python app_user/' + self.app_id + '.py')

def spawn_app(i):
    os.system('cd .. && source .env && python app_user/' + i + '.py')
    # os.system('bash .env && python app_user/' + i + '.py')

def callback(ch, method, properties, body):
    # print("\nRABBITMQ app_manager, Received %r" % body)
    kind = body.decode().split(',')
    # print(kind)
    if kind[0] == 'app_upload':
        print('uploading..')
        # os.system('ls')
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
        # print('kind[1]', kind[1])
        # query = session.query(AppModel).filter_by(id=kind[1]).first() # 얘 반응이 느리다..왜지?
        # print('query2', query.app_switch)
        # print('swt', kind[2])

        session.commit()
        if 'False' == kind[2]:
            conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
            ch = conn.channel()
            ch.queue_declare(queue='app_' + (kind[1]))
            ch.basic_publish(exchange='', routing_key='app_' + (kind[1]), body=(kind[1]) + ',' + (kind[2]))
            # print("RABBITMQ, Send " + str(kind[1]))
            ch.close()
            conn.close()

            # log
            query = session.query(AppModel).filter_by(app_id=kind[1]).first()
            app_title = query.app_name
            content = app_title+' 스위치 OFF'
            print(content)
            item = AppLog(content, kind[1], str(0), str(0),
                          str(datetime.datetime.utcnow()).split('.')[0])
            session.add(item)
            session.commit()
            c = session.query(AppLog).order_by('id').all()
            res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))

        else:
            # pt[int(kind[1])] = threading.Thread(target=spawn_app, args=(kind[1],))
            # pt[int(kind[1])].start()

            # pt = SpawnApp(kind[1])
            # pt.start()

            pt = Process(target=spawn_app, args=(kind[1],))
            pt.start()

            # log
            query = session.query(AppModel).filter_by(app_id=kind[1]).first()
            app_title = query.app_name
            content = app_title+' 스위치 ON'
            print(content)
            item = AppLog(content, kind[1], str(0), str(0),
                          str(datetime.datetime.utcnow()).split('.')[0])
            session.add(item)
            session.commit()
            c = session.query(AppLog).order_by('id').all()
            res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))




        # session.commit()
        # query = session.query(AppModel).filter_by(id=kind[1]).first()
        # print('query3', query.app_switch)
        # session.close()


        # 됨
        # os.system('cd .. && source .env && python app_user/' + kind[1] + '.py')
        # pt = threading.Thread(target=spawn_app, args=(kind[1],))
        # pt.start()


        # print('threading.activeCount()', threading.activeCount())
        # print('threading.currentThread()', threading.currentThread())
        # print('threading.enumerate()', threading.enumerate())
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

channel.basic_consume(callback, queue='loq_q', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
