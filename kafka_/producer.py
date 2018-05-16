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
        except Exception as e:
            print('Try for %s' % (n))
            print(e)
    print('Kafka Brokers are unavailable')
    return None

def insert_armor(armor):
    producer = get_producer()
    producer.send('armor-insert', json.dumps(armor).encode())
    producer.close()

def delete_armor(id):
    producer = get_producer()
    producer.send('delete_armor', json.dumps(id).encode())
    producer.close()

def insert_weapon(weapon):
    producer = get_producer()
    producer.send('insert_weapon', json.dumps(weapon).encode())
    producer.close()

def delete_weapon(id):
    producer = get_producer()
    producer.send('delete_weapon', json.dumps(id).encode())
    producer.close()

def insert_item(item):
    producer = get_producer()
    producer.send('insert_item', json.dumps(item).encode())
    producer.close()

def delete_item(id):
    producer = get_producer()
    producer.send('delete_item', json.dumps(id).encode())
    producer.close()

def insert_decoration(decoration):
    producer = get_producer()
    producer.send('inser_decoration', json.dumps(decoration).encode())
    producer.close()

def delete_decoration(id):
    producer = get_producer()
    producer.send('delete_decoration', json.dumps(id).encode())
    producer.close()

def add_build(user, build_id):
    producer = get_producer()
    add_build_msg = {'user' : user, 'build_id' : build_id}
    producer.send('add-build', json.dumps(add_build_msg).encode())
    producer.close()

def delete_build(user, build_id, build_parts):
    producer = get_producer()
    delete_build_msg = {'user' : user, 'build_id' : build_id, 'build_parts' : build_parts}
    producer.send('delete-build', json.dumps(delete_build_msg).encode())
    producer.close()

def add_user(user):
    producer = get_producer()
    add_user_msg = {'user' : user}
    producer.send('add_user', json.dumps(add_user_msg).encode())
    producer.close()

def delete_user(user):
    producer = get_producer()
    delete_user_msg = {'user' : user}
    producer.send('delete_user', json.dumps(delete_user_msg).encode())
    producer.close()

def add_build_component(build_id, part, item_id):
    producer = get_producer()
    add_build_component_msg = {'build_id' : build_id, 'part' : part, 'item_id' : item_id}
    producer.send('add_build_component', json.dumps(add_build_component_msg).encode())
    producer.close()

def remove_build_component(part, build_id):
    producer = get_producer()
    remove_build_component_msg = {'part' : part, 'build_id' : build_id}
    producer.send('remove_build_component', json.dumps(remove_build_component_msg).encode())
    producer.close()

def add_decoration(build_id, part, item_id):
    producer = get_producer()
    add_decoration_msg = {'build_id' : build_id, 'part' : part, 'item_id' : item_id}
    producer.send('add_decoration', json.dumps(add_decoration_msg).encodes())
    producer.close()

def remove_decoration(build_id, part, item_id):
    producer = get_producer()
    remove_decoration_msg = {'build_id' : build_id, 'part' : part, 'item_id' : item_id}
    producer.send('remove_decoration', json.dumps(remove_decoration_msg).encodes())
    producer.close()

def remove_all_decorations(build_id, part):
    producer = get_producer()
    remove_all_decorations_msg = {'build_id' : build_id, 'part' : part}
    producer.send('remove_all_decorations_msg', json.dumps(remove_all_decorations_msg).encodes())
    producer.close()


