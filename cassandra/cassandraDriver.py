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
from cassandra.query import dict_factory

IP_ADDRESSES = ['137.112.89.78', '137.112.89.77', '137.112.89.76', '137.112.89.75']
KEYSPACE = 'buildhunter'
ARMOR_TABLE = 'armor'

def connect():
    global session
    try:
        cluster = Cluster(IP_ADDRESSES)
        session = cluster.connect()
        __createKeyspaceIfNotExists()
        session.set_keyspace(KEYSPACE)
        session.row_factory = dict_factory
    except Exception as e:
        log.error('Unable to connect to cassandra')
        log.exception(e)
        return None
    
def __createKeyspaceIfNotExists():
    rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
    if KEYSPACE in [row[0] for row in rows]:
        return
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
        """ % KEYSPACE)

def createArmorTable():
    session.execute("""
        create type if not exists skillmap (
            id int,
            name text,
            value int
        )
    """)

    session.execute("""
        create type if not exists craftmap (
            id int,
            name text,
            quantity int
        )
    """)

    session.execute("""
        create table if not exists %s (
        id int,
        name text,
        part text,
        price text,
        rarity int,
        slot int,
        type text,
        gender text,
        skill list<frozen<skillmap>>,
        crafting_item list<frozen<craftmap>>,
        defense map<text,int>,
        resist map<text, int>,
        PRIMARY KEY (id, name)
        )  
    """ % ARMOR_TABLE)



def insertArmor(armor):
    query = SimpleStatement("INSERT INTO " + ARMOR_TABLE + "(name, id, price, part, rarity, slot, type, gender, skill, crafting_item, defense, resist)" +
    "VALUES ('{name}', {id}, '{price}', '{part}', {rarity}, {slot}, '{type}', '{gender}', {skill}, {crafting_item}, {defense}, {resist})".format_map(armor))
    session.execute(query)