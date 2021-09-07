from os import environ
import faust
from faker import Faker


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


@app.agent(topic)
async def hello(persons):
    async for person in persons:
        print(f'Hello from {person.name}, {person.age} years.')


# @app.timer(interval=1.0)
# async def person_sender(app):
#     person = generate_person()
#     await hello.send(value=person)

if __name__ == '__main__':
    app.main()
