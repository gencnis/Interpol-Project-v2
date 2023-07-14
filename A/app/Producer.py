"""
Producer.py

This script contains a function to produce data by publishing it to a RabbitMQ queue.

Dependencies:
- pika: Python library for RabbitMQ integration
- json: Python library for working with JSON data

The main function 'produce' takes the data as input, establishes a connection with RabbitMQ, and publishes the data to a specific queue. It utilizes the pika library for RabbitMQ integration and the json library for converting the data into a JSON string.

@Author: Nisanur Genc
"""

import pika  # Import the pika library for RabbitMQ integration
import json  # Import the json library for working with JSON data

def produce(data):
    """
    Publishes the data to a RabbitMQ queue.

    Args:
        data: The data to be published.

    Returns:
        None
    """

    connection_parameters = pika.ConnectionParameters("rabbitmq")  # Define the connection parameters for RabbitMQ

    connection = pika.BlockingConnection(connection_parameters)  # Establish a connection with RabbitMQ

    channel = connection.channel()  # Create a channel

    channel.queue_declare(queue='box')  # Declare the queue 'box'

    message = json.dumps(data)  # Convert the data to a JSON string

    # Publish the message to the 'box' queue
    channel.basic_publish(exchange='', routing_key='box', body=message)

    print('sent message')

    connection.close()