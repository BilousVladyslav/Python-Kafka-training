from os import environ

from confluent_kafka import Consumer, KafkaException, TopicPartition

BROKER_URL = environ.get('BROKER_URL', '')
TOPIC = environ.get('TOPIC', '')
PARTITION_ID = int(environ.get('PARTITION_ID', 0))
GROUP_ID = environ.get('GROUP_ID', '')
HOSTNAME = 'consumer_' + environ.get('HOSTNAME', 'default')

# set up client id
# use assign instead of subscribe (what the difference)
# TODO: try manual commit
# TODO: 'auto.offset.reset': 'earliest' try latest
# TODO: need to try streams
# poll timeout (what is it)
# scale consumers (with different group id)


def assignation_report(consumer, p):
    print('Assigned partition:', p)


if __name__ == '__main__':
    conf = {
        'bootstrap.servers': BROKER_URL,
        'client.id': HOSTNAME,
        'group.id': GROUP_ID,
        'auto.offset.reset': 'earliest'
    }
    partition = TopicPartition(topic=TOPIC, partition=PARTITION_ID)
    consumer = Consumer(conf)
    # consumer.subscribe([TOPIC], on_assign=assignation_report)
    consumer.assign([partition])
    try:
        while True:
            msg = consumer.poll(timeout=0.5)
            if msg is None:
                continue
            if msg.error():
                raise KafkaException(msg.error())
            else:
                print(msg.topic(), msg.partition(), msg.offset(), msg.key(), msg.value())
    finally:
        consumer.close() # ... to commit final offsets.
