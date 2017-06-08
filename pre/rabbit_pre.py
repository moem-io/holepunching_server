# rabbit pre
from app.models.app_model import AppModel
import pika
import threading
from app import session

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

SW = True
input_sw = True
input_val = None

def callback(ch, method, properties, body):
    global SW
    global connection
    global channel
    global rabbit_app_id
    global input_sw
    global input_val

    kind = body.decode().split(',')
    if kind[0] == str(rabbit_app_id):
        # query = session.query(AppModel).filter_by(id=kind[0]).first()
        if 'False' == kind[1]:
            SW = False
            channel.close()
            connection.close()
            print('end app : '+str(rabbit_app_id))
        elif kind[1] == 'input':
            input_val = int(kind[2])
            input_sw = False

def rabbit():
    global connection
    global channel
    global rabbit_app_id

    channel.queue_declare(queue='app_'+str(rabbit_app_id))
    channel.basic_consume(callback, queue='app_'+str(rabbit_app_id), no_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

pt = threading.Thread(target=rabbit)
pt.start()