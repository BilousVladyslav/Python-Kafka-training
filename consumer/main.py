from os import environ

from confluent_kafka import Consumer, KafkaException

BROKER_URL = environ.get('BROKER_URL', '')
TOPIC = environ.get('TOPIC', '')
GROUP_ID = environ.get('GROUP_ID', '')

# set up client id
# use assign instead of subscribe (what the difference)
# try manual commit
# 'auto.offset.reset': 'earliest' try latest
# need to try streams
# poll timeout (what is it)
# scale consumers (with different group id)


def assignation_report(consumer, p):
    print('Assigned partition:', p)


if __name__ == '__main__':
    conf = {'bootstrap.servers': BROKER_URL, 'group.id': GROUP_ID, 'auto.offset.reset': 'earliest'}
    consumer = Consumer(conf)
    consumer.subscribe([TOPIC], on_assign=assignation_report)
    try:
        while True:
            msg = consumer.poll(timeout=1.0)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(msg.topic(), msg.partition(), msg.offset(), msg.key(), msg.value())
    finally:
        consumer.close() # ... to commit final offsets.
