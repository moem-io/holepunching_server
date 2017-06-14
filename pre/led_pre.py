# ledRun
import threading
import pika

# db
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
from app.models.nodes import Nodes
from app.models.sensor import Sensors
from app import session
from app.models.app_setting import AppSetting
from app.models.app_model import AppModel
import datetime
import json
from requests import post
from manager.make_app import AlchemyEncoder

def ledRun(input=90):
    global rabbit_app_id
    global SW
    global AppLog
    global output_log_kind
    global api_url


    if not SW:
        return 0

    # todo led 비교 후 내보내기
    # rgb = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
    # rgb_in = rgb.app_output_detail
    # if not rgb == input:
    if True:
        session.commit()

        sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()

        # save
        q = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
        q.app_output_detail = input
        session.commit()

        # log
        in_node = sett.in_node
        in_sensor = sett.in_sensor
        # content = 'App ' + str(rabbit_app_id) + ' : Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에 ' + \
        #           output_log_kind + ' ' + str(input) + ' 동작'
        content = 'Node [' + str(in_node) + ']의 Sensor[' + str(in_sensor) + ']에 ' + \
                  output_log_kind + ' ' + str(input) + ' 동작'
        print(content)
        item = AppLog(content, rabbit_app_id, str(in_node), str(in_sensor),
                      str(datetime.datetime.utcnow()).split('.')[0])
        session.add(item)
        session.commit()
        c = session.query(AppLog).order_by('id').all()
        res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))

        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='led_q')
        channel.basic_publish(exchange='',
                              routing_key='led_q',
                              body=str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + str(input))
        # print('led output :', input)
        print('')
        # print("RABBITMQ, led queue, Send " + str(input))
        connection.close()
