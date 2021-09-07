from os import environ
from dataclasses import dataclass

from confluent_kafka import Producer

BROKER_URL = environ.get('BROKER_URL', '')
TOPIC = environ.get('TOPIC', '')

# use objects instead of strings
# scale producers

@dataclass
class Dog:
    name: str
    age: int


def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')


if __name__ == '__main__':

    producer = Producer(**{'bootstrap.servers': BROKER_URL})
    for something in range(1000):
        try:
            producer.produce(TOPIC, str(something), callback=delivery_report)
        except BufferError:
            print("Local producer queue is full, try again")
        # Serve delivery callback queue.
        producer.poll(0)
        # Wait until all messages have been delivered
        producer.flush()
