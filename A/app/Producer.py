import pika
import json

def produce(data):

    connection_parameters = pika.ConnectionParameters("rabbitmq")

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.queue_declare(queue='letterbox')

    message = json.dumps(data)

    channel.basic_publish(exchange='', routing_key='letterbox', body=message)

    print('sent message')

    connection.close()