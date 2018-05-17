#!/usr/bin/env python

from kafka import KafkaProducer
import json
from pprint import pprint

nodes = ['433-05.csse.rose-hulman.edu:9092', '433-06.csse.rose-hulman.edu:9092', '433-07.csse.rose-hulman.edu:9092', '433-08.csse.rose-hulman.edu:9092']

def get_producer():
    for n in nodes:
        try:
            producer = KafkaProducer(bootstrap_servers=n)
            return producer
        except Exception:
            pass
    return None

def insert_armor(armor):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('insert_armor', json.dumps(armor).encode())
    producer.close()

def delete_armor(id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('delete_armor', json.dumps(id).encode())
    producer.close()

def insert_weapon(weapon):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('insert_weapon', json.dumps(weapon).encode())
    producer.close()

def delete_weapon(id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('delete_weapon', json.dumps(id).encode())
    producer.close()

def insert_item(item):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('insert_item', json.dumps(item).encode())
    producer.close()

def delete_item(id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('delete_item', json.dumps(id).encode())
    producer.close()

def insert_decoration(decoration):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('insert_decoration', json.dumps(decoration).encode())
    producer.close()

def delete_decoration(id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    producer.send('delete_decoration', json.dumps(id).encode())
    producer.close()

def add_build(user, build_id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    add_build_msg = {'user' : user, 'build_id' : build_id}
    producer.send('add_build', json.dumps(add_build_msg).encode())
    producer.close()

def delete_build(user, build_id, build_parts):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    delete_build_msg = {'user' : user, 'build_id' : build_id, 'build_parts' : build_parts}
    producer.send('delete_build', json.dumps(delete_build_msg).encode())
    producer.close()

def add_user(user):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    add_user_msg = {'user' : user}
    producer.send('add_user', json.dumps(add_user_msg).encode())
    producer.close()

def delete_user(user):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    delete_user_msg = {'user' : user}
    producer.send('delete_user', json.dumps(delete_user_msg).encode())
    producer.close()

def add_build_component(build_id, part, item_id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    add_build_component_msg = {'build_id' : build_id, 'part' : part, 'item_id' : item_id}
    producer.send('add_build_component', json.dumps(add_build_component_msg).encode())
    producer.close()

def remove_build_component(build_id, part):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    remove_build_component_msg = {'part' : part, 'build_id' : build_id}
    producer.send('remove_build_component', json.dumps(remove_build_component_msg).encode())
    producer.close()

def add_decoration(build_id, part, item_id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    add_decoration_msg = {'build_id' : build_id, 'part' : part, 'item_id' : item_id}
    producer.send('add_decoration', json.dumps(add_decoration_msg).encode())
    producer.close()

def remove_decoration(build_id, part, item_id):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    remove_decoration_msg = {'build_id' : build_id, 'part' : part, 'item_id' : item_id}
    producer.send('remove_decoration', json.dumps(remove_decoration_msg).encode())
    producer.close()

def remove_all_decorations(build_id, part):
    producer = get_producer()
    if producer == None:
        raise ConnectionError('Could not reach service')
    remove_all_decorations_msg = {'build_id' : build_id, 'part' : part}
    producer.send('remove_all_decorations', json.dumps(remove_all_decorations_msg).encode())
    producer.close()


