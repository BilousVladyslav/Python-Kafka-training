import json
from dataclasses import dataclass
from os import environ
from random import randint
from time import sleep

from confluent_kafka import Producer
from faker import Faker

BROKER_URL = environ.get('BROKER_URL', '')
TOPIC = environ.get('TOPIC', '')
MESSAGES_COUNT = int(environ.get('MESSAGES_COUNT', 10))
HOSTNAME = 'producer_' + environ.get('HOSTNAME', 'default')

# use objects instead of strings
# TODO: scale producers


@dataclass
class Person:
    name: str
    age: int

    def __bytes__(self):
        return json.dumps(self.__dict__).encode('utf-8')


def generate_persons(count: int) -> list[Person]:
    persons = list()
    fake = Faker()
    for _ in range(count):
        person = Person(fake.name(), randint(18, 100))
        persons.append(person)
    return persons


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


if __name__ == '__main__':
    config = {
        'bootstrap.servers': BROKER_URL,
        'client.id': HOSTNAME
    }

    producer = Producer(config)
    for person in generate_persons(MESSAGES_COUNT):
        try:
            producer.produce(TOPIC, bytes(person), callback=delivery_report)
        except BufferError:
            print("Local producer queue is full, try again")
        # Serve delivery callback queue.
        producer.poll(0)
        # Wait until all messages have been delivered
        producer.flush()

sleep(10)
