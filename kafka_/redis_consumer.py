#!/usr/bin/env python
import sys

sys.path.insert(0,'../redis_')

from confluent_kafka import Consumer, KafkaError
import json
import time
from pprint import pprint

from redis_ import redisDriver

topics = ["add-build"]
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
            if not red.ping():
                time.sleep(1)
                continue
            msg = c.poll(0.1)
            # No message present
            if msg is None:
                continue
            # Found message
            elif not msg.error():
                # Try to handle
                result = insert_build(msg.value())
                if result:
                    pprint('Added Successfully ' + msg.value())
                    c.commit()
                else:
                    c.unsubscribe()
                    c.subscribe(topics)
                    print('Error Occurred Adding to Redis')
            elif msg.error().code() == KafkaError._PARTITION_EOF:
                print('End of partition reached {0}/{1}'.format(msg.topic(), msg.partition()))
            else:
                print('Error occurred: {0}'.format(msg.error().str()))
            time.sleep(1)

    except KeyboardInterrupt:
        pass
    
    finally:
        c.close()
        
                           
def insert_build(msg):
    args = json.loads(msg)
    try:
        red.add_build(args['user'], args['build_id'])
        return True
    except:
        return False


def main():
    print('Starting Redis Consumer')
    global red
    red = redisDriver.RedisDriver()
    repl()


if __name__ == "__main__":
    main()