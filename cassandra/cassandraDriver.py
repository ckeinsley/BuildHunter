#!/usr/bin/env python

# Utility Imports
import logging
log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Cassandra Driver
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement

IP_ADDRESSES = ['137.112.89.78', '137.112.89.77', '137.112.89.76', '137.112.89.75']
ARMOR_KEYSPACE = 'armor'
WEAPON_KEYSPACE = 'weapon'

def connect():
    global session
    try:
        cluster = Cluster(IP_ADDRESSES)
        session = cluster.connect()
    except Exception as e:
        log.error('Unable to connect to cassandra')
        log.exception(e)
        return None
    


def insertArmor(armor):
    2 + 2
