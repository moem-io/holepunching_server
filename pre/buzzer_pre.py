# buzzerRun
import threading
import pika
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

def buzzerRun(in_val='xx'):
    global rabbit_app_id
    global SW
    global AppLog
    global output_log_kind
    global api_url

    if True:
        session.commit()
        sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()

        # save
        q = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
        q.app_output_detail = in_val
        session.commit()

        # log
        out_node = sett.out_node
        out_sensor = sett.out_sensor
        content = 'Node [' + str(out_node) + ']의 Sensor[' + str(out_sensor) + ']에 ' + \
                  output_log_kind + ' ' + in_val + ' 동작'
        print(content)
        item = AppLog(content, rabbit_app_id, str(out_node), str(out_sensor),
                      str(datetime.datetime.utcnow()).split('.')[0])
        session.add(item)
        session.commit()
        c = session.query(AppLog).order_by('id').all()
        res = post(api_url + 'app/log/save', data=json.dumps(c, cls=AlchemyEncoder))

        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='buzzer_q')
        channel.basic_publish(exchange='',
                              routing_key='buzzer_q',
                              body=str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + in_val)
        print('')
        connection.close()
