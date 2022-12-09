import json
import os

import pika
from functools import partial
import logging

from sqlalchemy import create_engine
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB = os.environ.get('POSTGRES_DB')
AMQP_URL = os.environ.get('AMQP_URL')

db_string = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@db:5432/{POSTGRES_DB}"
db = create_engine(db_string)
base = declarative_base()

Session = sessionmaker(db)
session = Session()


class PikaClient:
    def __init__(self, queue):
        self.queue = queue
        parametrs = pika.URLParameters(AMQP_URL)
        self.connection = pika.BlockingConnection(parametrs)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue, durable=True)
        self.channel.basic_qos(prefetch_count=1)


class Complaint(base):
    __tablename__ = 'complaint'

    complaint_id = Column(Integer, primary_key=True)
    last_name = Column(String(50), nullable=True)
    first_name = Column(String(50), nullable=True)
    patronymic = Column(String(50))
    phone = Column(String(20), nullable=True)
    complaint_text = Column(Text, nullable=True)


def callback(ch, method, properties, body):
    data = json.loads(body.decode("UTF-8"))

    ch.basic_ack(delivery_tag=method.delivery_tag)

    try:
        logging.warning("1") 
        new_complaint = Complaint(last_name=data["last_name"],
                                  first_name=data["first_name"],
                                  patronymic=data["patronymic"],
                                  phone=data["phone"],
                                  complaint_text=data["complaint_text"])
        logging.warning("2") 
        session.add(new_complaint)
        logging.warning("3") 
        session.commit()
        logging.warning("good") 
    except Exception as e:
        logging.warning(e) 
        logging.warning(db_string) 
        session.rollback()


def main():
    try:
        QUEUE = 'task_queue'
        consumer = PikaClient(queue=QUEUE)
        consumer.channel.basic_consume(queue=QUEUE, on_message_callback=callback)

        consumer.channel.start_consuming()
    except pika.exceptions.AMQPConnectionError:
        pass


if __name__ == "__main__":
    main()
