import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='app_q')
# channel.queue_declare(queue='app_q') # 한개만 됨

def callback(ch, method, properties, body):
    print(" RABBITMQ app_manager, Received %r" % body)

channel.basic_consume(callback, queue='app_q', no_ack=True)
print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()