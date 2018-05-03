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
ARMOR_CRAFTING_TABLE = 'crafting'
SKILL_TABLE = 'skills'

WEAPON_TABLE = 'weapon'
WEAPON_UPGRADES_TO_TABLE = 'upgradesto'
WEAPON_UPGRADE_ITEMS_TABLE = 'upgradeitems'
WEAPON_CREATE_ITEMS_TABLE = 'createitems'


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
    """ % ARMOR_CRAFTING_TABLE)

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
    armorQuery = SimpleStatement("INSERT INTO " + ARMOR_TABLE + 
        "(id, part, name, price, rarity, slot, type, gender, fire, dragon, thunder, water, ice, defense_init, defense_max)"+
        "VALUES ({id}, '{part}', '{name}', '{price}', {rarity}, {slot}, '{type}', '{gender}', {fire}, {dragon}, {thunder}, {water}, {ice}, {defense_init}, {defense_max})".format_map(armor)
    )
    session.execute(armorQuery)
    
    for skill in skills:
        skillsQuery = SimpleStatement("INSERT INTO " + SKILL_TABLE + 
            "(id, skill_id, name, value) VALUES ({id}, {skill_id}, '{name}', {value})".format_map(skill)
        )
        session.execute(skillsQuery)

    for item in crafting:
        craftsQuery = SimpleStatement("INSERT INTO " + ARMOR_CRAFTING_TABLE + 
            """
            (id, item_id, name, quantity)
            VALUES ({id}, {item_id}, '{name}', {quantity})
            """.format_map(item)
        )
        session.execute(craftsQuery)


def createWeaponTable():
    session.execute("""
        create table if not exists %s (
        id int,
        name text,
        affinity int,
        create_price text,
        defense int,
        glaive_type text,
        phial text,
        rarity int,
        shelling text,
        slot int, 
        true_attack int,
        upgrade_price text,
        weapon_family text,
        class text,
        PRIMARY KEY (id)
        )  
    """ % WEAPON_TABLE)

    session.execute("""
        create table if not exists %s (
        id int,
        item_id int,
        name text,
        quantity int,
        primary key (id, item_id)
        )  
    
    """ % WEAPON_CREATE_ITEMS_TABLE)

    session.execute("""
        create table if not exists %s (
        id int,
        item_id int,
        name text,
        quantity int,
        primary key (id, item_id)
        )  
    
    """ % WEAPON_UPGRADE_ITEMS_TABLE)

    session.execute("""
        create table if not exists %s (
        id int,
        item_id int,
        name text,
        primary key (id, item_id)
        )  
    
    """ % WEAPON_UPGRADES_TO_TABLE) 

def insertWeapon(weaponToInsert, createItems, upgradeItems, upgradesTo):
    __insertWeaponToTable(weaponToInsert)

def __insertWeaponToTable(weaponToInsert):
    session.execute("INSERT INTO " + WEAPON_TABLE + """
    (id, name, affinity, create_price, defense, glaive_type, phial, rarity,
    shelling, slot, true_attack, upgrade_price, weapon_family, class)
    VALUES({id}, {affinity}, '{create_price}', {defense}, '{glaive_type}',
    '{phial}', {rarity}, '{shelling}', {slot}, {true_attack}, '{upgrade_price}',
    '{weapon_family}', '{class}')
    """.format_map(weaponToInsert))