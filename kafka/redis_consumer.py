#!/usr/bin/env python
import sys

sys.path.insert(0,'../redis')

from confluent_kafka import Consumer, KafkaError
import json
import time

from redisDriver import RedisDriver

topics = ["build-insert", 
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
            if not db.ping():
                time.sleep(1)
                continue
            msg = c.poll(0.1)
            # No message present
            if msg is None:
                continue
            # Found message
            elif not msg.error():
                # Try to handle
                
                
def 


def main():
    print('Starting Redis Consumer')
    global db = RedisDriver()
    repl()


if __name__ == "__main__":
    main()       