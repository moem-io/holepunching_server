# rabbit pre
from app.models.app_model import AppModel
import pika
import threading
from app import session

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

SW = True
def callback(ch, method, properties, body):
    global SW
    global connection
    global channel
    global rabbit_app_id

    kind = body.decode().split(',')
    if kind[0] == str(rabbit_app_id):
        query = session.query(AppModel).filter_by(id=kind[0]).first()
        if 'False' == kind[1]:
            sw = False
            channel.close()
            connection.close()
            print('get'+str(rabbit_app_id))

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