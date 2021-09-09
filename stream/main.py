import logging
from os import environ

import faust
from faker import Faker
from faust.types import TP

BROKER_URL = environ.get('BROKER_URL', '')
TOPIC = environ.get('TOPIC', '')
PARTITION_ID = int(environ.get('PARTITION_ID', 0))
GROUP_ID = environ.get('GROUP_ID', '')
HOSTNAME = 'stream_' + environ.get('HOSTNAME', 'default')


class Person(faust.Record):
    name: str
    age: int


def generate_person() -> Person:
    fake = Faker()
    return Person(fake.name(), fake.pyint(min_value=18, max_value=100))


app = faust.App(GROUP_ID, broker=f'kafka://{BROKER_URL}')
topic = app.topic(TOPIC, value_type=Person)


# @app.task()
# async def on_start():
#     tp = TP(TOPIC, PARTITION_ID)
#     await app.consumer.seek(tp, 272100)


@app.agent(topic)
async def hello(persons_stream):
    async for event in persons_stream.noack().events():
        logging.info(f'Hello from {event.message.offset} offset')
        async with event:
            logging.info(f'{event.message.offset} offset manual ack')


@app.command()
async def person_sender():
    person = generate_person()
    await hello.send(value=person)

if __name__ == '__main__':
    app.main()
