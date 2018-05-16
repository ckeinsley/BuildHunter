#!/usr/bin/env python
import sys

sys.path.insert(0,'../redis_')

from confluent_kafka import Consumer, KafkaError
import json
import time
from pprint import pprint

from redis_ import redisDriver

topics = ['add_build', 'delete_build', 'add_user', 'delete_user', 'add_build_component', 'remove_build_component', 'add_decoration', 'remove_decoration', 'remove_all_decorations']
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
                if msg.topic() == u'add_build':
                    result = add_build(msg.value())
                elif msg.topic() == u'delete_build':
                    result = delete_build(msg.value())
                elif msg.topic() == u'add_user':
                    result = add_user(msg.value())
                elif msg.topic() == u'delete_user':
                    result = delete_user(msg.vlaue())
                elif msg.topic() == u'add_build_component':
                    result = add_build_component(msg.value())
                elif msg.topic() == u'remove_build_component':
                    result = remove_build_component(msg.value())
                elif msg.topic() == u'add_decoration':
                    result = add_decoration(msg.value())
                elif msg.topic() == u'remove_decoration':
                    result = remove_decoration(msg.value())
                elif msg.topic() == u'remove_all_decorations':
                    result = remove_all_decorations(msg.value())
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
        
                           
def add_build(msg):
    args = json.loads(msg)
    try:
        red.add_build(args['user'], args['build_id'])
        return True
    except Exception as e:
        return False

def delete_build(msg):
    args = json.loads(msg)
    try:
        red.delete_build(args['user'], args['build_id'], args['build_parts'])
        return True
    except Exception as e:
        return False

def add_user(msg):
    args = json.loads(msg)
    try:
        red.add_user(args['user'])
        return True
    except Exception as e:
        return False

def delete_user(msg):
    args = json.loads(msg)
    try:
        red.delete_user(args['user'])
        return True
    except Exception as e:
        return False

def add_build_component(msg):
    args = json.loads(msg)
    try:
        red.add_build_component(args['build_id'], args['part'], args['item_id'])
    except Exception as e:
        return False

def remove_build_component(msg):
    args = json.loads(msg)
    try:
        red.remove_build_component(args['part'], args['build_id'])
    except Exception as e:
        return False

def add_decoration(msg):
    args = json.loads(msg)
    try:
        red.add_decoration(args['build_id'], args['part'], args['item_id'])
    except Exception as e:
        return False

def remove_decoration(msg):
    args = json.loads(msg)
    try:
        red.remove_decoration(args['build_id'], args['part'], args['item_id'])
    except Exception as e:
        return False

def remove_all_decorations(msg):
    args = json.loads(msg)
    try:
        red.remove_all_decorations(args['build_id'], args['part'])
    except Exception as e:
        return False



def main():
    print('Starting Redis Consumer')
    global red
    red = redisDriver.RedisDriver()
    repl()


if __name__ == "__main__":
    main()