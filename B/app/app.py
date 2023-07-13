# app.py
import json
import pika
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)


class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    nationalities = db.Column(db.String(100))
    date_of_birth = db.Column(db.String(100))
    image_link = db.Column(db.String(1000))

    def __repr__(self):
        return f"Person(id={self.id}, name={self.name}, lastname={self.lastname}, " \
               f"nationalities={self.nationalities}, date_of_birth={self.date_of_birth}, image_link={self.image_link})"


@app.route('/')
def index():
    """Render the index.html template for the home page."""
    return render_template('index.html')


@app.route('/filter', methods=['POST'])
def filter_data():
    """Filter the data based on the provided criteria and return the results."""
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    nationalities = request.form.get('nationalities')
    date_of_birth = request.form.get('date_of_birth')
    image_link = request.form.get('image_link')

    # Filter the data based on the provided criteria
    filtered_data = Person.query
    if name:
        filtered_data = filtered_data.filter(Person.name.ilike(f"%{name}%"))
    if lastname:
        filtered_data = filtered_data.filter(Person.lastname.ilike(f"%{lastname}%"))
    if nationalities:
        filtered_data = filtered_data.filter(Person.nationalities.ilike(f"%{nationalities}%"))
    if date_of_birth:
        filtered_data = filtered_data.filter(Person.date_of_birth.ilike(f"%{date_of_birth}%"))
    if image_link:
        filtered_data = filtered_data.filter(Person.image_link.ilike(f"%{image_link}%"))

    results = filtered_data.all()

    return render_template('results.html', results=results)


def consume_data():
    """Consume data from RabbitMQ and store it in the database."""
    connection_parameters = pika.ConnectionParameters("rabbitmq")
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='letterbox')

    def callback(ch, method, properties, body):
        # Decode the message body
        data = json.loads(body.decode())
        
        # Store the data in the database
        person = Person(
            name=data['name'],
            lastname=data['lastname'],
            nationalities=data['nationalities'],
            date_of_birth=data['date_of_birth'],
            image_link=data['image_link']
        )
        db.session.add(person)
        db.session.commit()

    # Set up the callback function to consume messages from the 'letterbox' queue
    channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=callback)

    # Start consuming messages from the RabbitMQ queue
    print("Starting consuming")
    channel.start_consuming()


if __name__ == '__main__':
    # Create the database tables if they don't exist
    db.create_all()

    # Consume data from RabbitMQ
    consume_data()

    # Run the Flask application in debug mode
    app.run(debug=True)
