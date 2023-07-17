import pika
import time

class RabbitMQConnection:
    def __init__(self, hostname, port, queue_name):
        self.hostname = hostname
        self.port = port
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.connected = False

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.hostname, port=self.port))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue_name)
            self.connected = True
            print("Connection to RabbitMQ established.")
        except pika.exceptions.AMQPConnectionError as e:
            print("Failed to connect to RabbitMQ:", e)

    def is_connected(self):
        return self.connected

    def check_connection(self):
        if not self.is_connected():
            print("Connection lost. Attempting to reconnect...")
            self.connect()

    def publish_data(self, data):
        if self.is_connected():
            try:
                # Publish data to the RabbitMQ queue
                self.channel.basic_publish(exchange='',
                                            routing_key=self.queue_name,
                                            body=str(data))
                print("Data published to RabbitMQ:", data)
            except pika.exceptions.AMQPConnectionError as e:
                print("Failed to publish data. Connection error:", e)
            except pika.exceptions.AMQPChannelError as e:
                print("Failed to publish data. Channel error:", e)
