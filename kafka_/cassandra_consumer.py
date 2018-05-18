import sys

# Cassandra Driver
sys.path.insert(0,'../cassandra_')
import cassandraDriver as db


from confluent_kafka import Consumer, KafkaError
import json
import time
from pprint import pprint

topics = ["insert_armor", "insert_weapon"]
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
    c.subscribe(topics)
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
                # Which message was it?
                if msg.topic() == u'insert_armor':
                    insert_armor(msg, c)
                elif msg.topic() == u'insert_weapon':
                    insert_weapon(msg, c)
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

def insert_armor(msg, c):
    result = insertArmor(msg.value())
    checkResult(result, msg, c) 

def insert_weapon(msg, c):
    result = insertWeapon(msg.value())
    checkResult(result, msg, c)

def checkResult(result, msg, c):
    if result: 
        pprint('Added Successfully ' + msg.value())
        c.commit()
    else:
        c.unsubscribe()
        c.subscribe(topics)
        print('Error Occurred Adding to Cassandra')


def verifyCassandraHeartbeat():
    return db.heartBeat()

#Attempt to insert the armor. If no errors occur, we can commit
def insertArmor(msg):
    armor = json.loads(msg)
    try:
        db.insertArmor(armor)
        return True
    except Exception as e:
        print(e)
        return False

def insertWeapon(msg):
    armor = json.loads(msg)
    try:
        db.insertWeapon(armor)
        return True
    except Exception as e:
        print(e)
        return False

def main():
    print('Starting Cassandra Consumer')
    repl()


if __name__ == "__main__":
    main()