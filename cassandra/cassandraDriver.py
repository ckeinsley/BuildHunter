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
CRAFTING_TABLE = 'crafting'
SKILL_TABLE = 'skills'

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
        create table if not exists %s (
        id int,
        name text,
        part text,
        price text,
        rarity int,
        slot int,
        type text,
        gender text,
        fire int,
        dragon int,
        thunder int,
        water int,
        ice int,
        defense_init int,
        defense_max int,
        PRIMARY KEY (id)
        )  
    """ % ARMOR_TABLE)

    session.execute("""
        create table if not exists %s (
        id int,
        item_id int,
        name text,
        quantity int,
        primary key (id, item_id)
        )  
    """ % CRAFTING_TABLE)

    session.execute("""
        create table if not exists %s (
        id int,
        skill_id int,
        name text,
        value int,
        primary key (id, skill_id)
        )  
    """ % SKILL_TABLE)

def insertArmor(armor, skills, crafting):
    print(armor)
    armorQuery = SimpleStatement("INSERT INTO " + ARMOR_TABLE + 
        "(id int, part text, name text, price text, rarity int, slot int, type text, gender text, fire int, dragon int, thunder int, water int, ice int, defense_init int, defense_max int)"+
        "VALUES ('{id}', '{part}', '{name}', '{price}', {rarity}, {slot}, '{type}', '{gender}', {fire}, {dragon}, {thunder}, {water}, {ice}, {defense_init}, {defense_max})".format(**armor)
    )
    session.execute(armorQuery)
    
    for skill in skills:
        skillsQuery = SimpleStatement("INSERT INTO " + SKILL_TABLE + 
            """
            (id, skill_id, name, value)
            VALUES ('{id}', '{skill_id}', {name}, '{value}')
            """.format_map(skill)
        )
        session.execute(skillsQuery)

    for item in crafting:
        craftsQuery = SimpleStatement("INSERT INTO " + CRAFTING_TABLE + 
            """
            (id, item_id, name, quantity)
            VALUES ('{id}', '{item_id}', {name}, '{quantity}')
            """.format_map(item)
        )
        session.execute(craftsQuery)
