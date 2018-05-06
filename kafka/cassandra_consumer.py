import sys

# Cassandra Driver
sys.path.insert(0,'../cassandra')
import cassandraDriver as db


from confluent_kafka import Consumer, KafkaError
import json
import time

topic = "armor-insert"
settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'buildHunter',
    'client.id': 'cassandra',
    'enable.auto.commit': False,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'smallest'}
}


def repl():
    c = Consumer(settings)
    c.subscribe([topic])
    try:
        while True:
            if not verifyCassandraHeartbeat():
                db.connect()
                continue
            msg = c.poll(0.1)
            if msg is None:
                continue
            elif not msg.error():
                insertArmor(msg.value())
                print('Received message: {0}'.format(msg.value()))
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                    .format(msg.topic(), msg.partition()))
            else:
                print('Error occurred: {0}'.format(msg.error().str()))
            time.sleep(10)

    except KeyboardInterrupt:
        pass

    finally:
        c.close()

def verifyCassandraHeartbeat():
    return db.heartBeat()

def insertArmor(msg):
    armor = json.loads(msg)
    db.insertArmor(armor)


def main():
    print('Starting Cassandra Consumer')
    repl()


if __name__ == "__main__":
    main()