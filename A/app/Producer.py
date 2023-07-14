import pika
import json

def produce(data):

    connection_parameters = pika.ConnectionParameters("rabbitmq")

    connection = pika.BlockingConnection(connection_parameters)

    channel = connection.channel()

    channel.queue_declare(queue='box')

    message = json.dumps(data)

    # Publish the message to the 'letterbox' queue
    channel.basic_publish(exchange='', routing_key='box', body=message)

    print('sent message')

    connection.close()