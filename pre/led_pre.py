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


def ledRun(input=90):
    global rabbit_app_id
    global SW
    if not SW:
        return 0

    # todo led 비교 후 내보내기
    # rgb = session.query(AppModel).filter_by(app_id=rabbit_app_id).first()
    # rgb_in = rgb.app_output_detail
    # if not rgb == input:
    if True:
        sett = session.query(AppSetting).filter_by(app_id=rabbit_app_id).first()
        # rabbit
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='led_q')
        channel.basic_publish(exchange='',
                              routing_key='led_q',
                              body=str(sett.out_node) + ',' + str(sett.out_sensor) + ',' + str(input))
        print('led output :', input)
        print('')
        # print("RABBITMQ, led queue, Send " + str(input))
        connection.close()
