import sys

# Cassandra Driver
sys.path.insert(0,'../cassandra')
import cassandraDriver as db


from confluent_kafka import Consumer, KafkaError
import json
import time
from pprint import pprint

topic = "armor-insert"
settings = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'buildHunter',
    'client.id': 'cassandra',
    'enable.auto.commit': False,
    'session.timeout.ms': 6000,
    'default.topic.config': {'auto.offset.reset': 'latest'}
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
            # No message present
            if msg is None:
                continue
            # Found a message
            elif not msg.error():
                # Try to insert
                result = insertArmor(msg.value())
                if result: 
                    pprint('Added Successfully ' + msg.value())
                    c.commit()
                else:
                    c.unsubscribe()
                    c.subscribe([topic])
                    print('Error Occurred Adding to Cassandra')
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'
                    .format(msg.topic(), msg.partition()))
            else:
                print('Error occurred: {0}'.format(msg.error().str()))
            time.sleep(1)

    except KeyboardInterrupt:
        pass

    finally:
        c.close()

def verifyCassandraHeartbeat():
    return db.heartBeat()

#Attempt to insert the armor. If no errors occur, we can commit
def insertArmor(msg):
    armor = json.loads(msg)
    try:
        db.insertArmor(armor)
        return True
    except:
        return False

def main():
    print('Starting Cassandra Consumer')
    repl()


if __name__ == "__main__":
    main()