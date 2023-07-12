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
    image_link = db.Column(db.String(200))

    def __repr__(self):
        return f"Person(id={self.id}, name={self.name}, lastname={self.lastname}, " \
               f"nationalities={self.nationalities}, date_of_birth={self.date_of_birth}, image_link={self.image_link})"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/filter', methods=['POST'])
def filter_data():
    name = request.form.get('name')
    lastname = request.form.get('lastname')
    nationalities = request.form.get('nationalities')
    date_of_birth = request.form.get('date_of_birth')
    image_link = request.form.get('image_link')

    # Filter the data based on the provided criteria
    filtered_data = Person.query
    if name:
        filtered_data = filtered_data.filter_by(name=name)
    if lastname:
        filtered_data = filtered_data.filter_by(lastname=lastname)
    if nationalities:
        filtered_data = filtered_data.filter_by(nationalities=nationalities)
    if date_of_birth:
        filtered_data = filtered_data.filter_by(date_of_birth=date_of_birth)
    if image_link:
        filtered_data = filtered_data.filter_by(image_link=image_link)

    results = filtered_data.all()

    return render_template('results.html', results=results)


def consume_data():
    connection_parameters = pika.ConnectionParameters("rabbitmq")
    connection = pika.BlockingConnection(connection_parameters)
    channel = connection.channel()
    channel.queue_declare(queue='letterbox')

    def callback(ch, method, properties, body):
        data = json.loads(body.decode())
        # Store the data in the database
        person = Person(name=data['name'], lastname=data['lastname'], nationalities=data['nationalities'],
                        date_of_birth=data['date_of_birth'], image_link=data['image_link'])
        db.session.add(person)
        db.session.commit()

    channel.basic_consume(queue='letterbox', auto_ack=True, on_message_callback=callback)
    print("Starting consuming")
    channel.start_consuming()


if __name__ == '__main__':
    db.create_all()
    consume_data()
    app.run(debug=True)
