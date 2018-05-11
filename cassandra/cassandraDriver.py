#!/usr/bin/env python

# Utility Imports
import logging
from datetime import datetime
log = logging.getLogger()
log.setLevel('DEBUG')
handler = logging.FileHandler('cassandra_driver.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Cassandra Driver
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement
from cassandra.query import dict_factory
import cassandra_weapon_conversion as convert

IP_ADDRESSES = ['137.112.89.78', '137.112.89.77', '137.112.89.76', '137.112.89.75']
KEYSPACE = 'buildhunter'

# Table Names
ARMOR_TABLE = 'armor'
ARMOR_CRAFTING_TABLE = 'crafting'
SKILL_TABLE = 'skills'

WEAPON_TABLE = 'weapon'
WEAPON_UPGRADES_TO_TABLE = 'upgradesto'
WEAPON_UPGRADE_ITEMS_TABLE = 'upgradeitems'
WEAPON_CREATE_ITEMS_TABLE = 'createitems'

PREPARED_QUERIES = {
    'ARMOR_ALL':'select * from armor where id=?',
    'WEAPON_ALL': 'select * from weapon where id=?',
    'BUILD_TOTAL_DEFENSE': 'select sum(defense_max) from armor where id in ?;',
    'BUILD_TOTAL_RESISTANCE': 'select sum(dragon) as dragon, sum(fire) as fire, sum(ice) as ice, sum(thunder) as thunder, sum(water) as water from armor WHERE id in ?',
    'BUILD_SKILLS': 'select name, value, skill_id from skills where id in ?'
}


def connect():
    global session
    try:
        cluster = Cluster(IP_ADDRESSES)
        session = cluster.connect()
        __createKeyspaceIfNotExists()
        session.set_keyspace(KEYSPACE)
        session.row_factory = dict_factory
        __createHeartBeatTable()
    except Exception as e:
        log.error('Unable to connect to cassandra')
        log.exception(e)
        return None
    __prepareStatements()

def __prepareStatements():
    for (name, query) in PREPARED_QUERIES.items():
        PREPARED_QUERIES[name] = session.prepare(query)

def __createHeartBeatTable():
    session.execute("CREATE TABLE IF NOT EXISTS heart (stamp timestamp, id text, PRIMARY KEY(id))")
    session.execute("INSERT INTO heart (id, stamp) VALUES ('last', toTimestamp(now()))")

def heartBeat():
    try:
        session.execute("SELECT * from heart")
        return True
    except:
        return False


def __createKeyspaceIfNotExists():
    rows = session.execute("SELECT keyspace_name FROM system_schema.keyspaces")
    if KEYSPACE in [row[0] for row in rows]:
        return
    session.execute("""
        CREATE KEYSPACE %s
        WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '3' }
        """ % KEYSPACE)

# ========================= CREATION ==============================================
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

def insertArmor(armor):
    armorToInsert = convert.convertArmor(armor)
    skills = convert.convertSkills(armor)
    crafting = convert.convertCrafting(armor)

    armorQuery = SimpleStatement("INSERT INTO " + ARMOR_TABLE + 
        "(id, part, name, price, rarity, slot, type, gender, fire, dragon, thunder, water, ice, defense_init, defense_max)"+
        "VALUES ({id}, '{part}', '{name}', '{price}', {rarity}, {slot}, '{type}', '{gender}', {fire}, {dragon}, {thunder}, {water}, {ice}, {defense_init}, {defense_max})".format(**armorToInsert)
    )
    result = session.execute(armorQuery)
    
    for skill in skills:
        skillsQuery = SimpleStatement("INSERT INTO " + SKILL_TABLE + 
            "(id, skill_id, name, value) VALUES ({id}, {skill_id}, '{name}', {value})".format(**skill)
        )
        session.execute(skillsQuery)

    for item in crafting:
        craftsQuery = SimpleStatement("INSERT INTO " + ARMOR_CRAFTING_TABLE + 
            """
            (id, item_id, name, quantity)
            VALUES ({id}, {item_id}, '{name}', {quantity})
            """.format(**item)
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
        attack int,
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
    __insertCreateItems(createItems)
    __insertUpgradeItems(upgradeItems)
    __insertUpgradesTo(upgradesTo)

def __insertWeaponToTable(weaponToInsert):
    (identifiers, values) = __findOptionalFields(weaponToInsert)
    query = "INSERT INTO " 
    query += WEAPON_TABLE 
    query += """
    (id, name, affinity, defense, rarity, slot, true_attack, weapon_family,
    class, attack""" 
    query += identifiers 
    query += """VALUES( {id}, '{name}', {affinity}, {defense}, {rarity}, {slot}, {true_attack},
    '{weapon_family}', '{class}', {attack}""".format_map(weaponToInsert) 
    query += values

    session.execute(query)

def __findOptionalFields(weaponToInsert):
    identifiers = ""
    values = ""
    glaive_type = weaponToInsert.get('glaive_type')
    if glaive_type:
        identifiers += ", glaive_type"
        values += ", '"+ glaive_type + "'"
    phial = weaponToInsert.get('phial')
    if phial:
        identifiers += ", phial"
        values += ", '" + phial + "'"
    create_price = weaponToInsert.get('create_price')
    if create_price:
        identifiers += ", create_price"
        values += ", '" + create_price + "'"
    upgrade_price = weaponToInsert.get('upgrade_price')
    if upgrade_price:
        identifiers += ", upgrade_price"
        values += ", '" + upgrade_price +"'"
    shelling = weaponToInsert.get('shelling')
    if shelling:
        identifiers += ", shelling"
        values += ", '" + shelling + "'"
    identifiers += ") " 
    values += ")"
    
    return (identifiers, values)

def __insertCreateItems(createItems):
    for item in createItems:
        session.execute("INSERT INTO " + WEAPON_CREATE_ITEMS_TABLE + 
            """(id, item_id, name, quantity) 
            VALUES({id}, {item_id}, '{name}', {quantity})""".format_map(item))

def __insertUpgradeItems(upgradeItems):
    for item in upgradeItems:
        session.execute("INSERT INTO " + WEAPON_UPGRADE_ITEMS_TABLE + 
            """(id, item_id, name, quantity) 
            VALUES({id}, {item_id}, '{name}', {quantity})""".format_map(item))

def __insertUpgradesTo(upgradesTo):
    for item in upgradesTo:
        session.execute("INSERT INTO " + WEAPON_UPGRADES_TO_TABLE + 
            """(id, item_id, name) 
            VALUES({id}, {item_id}, '{name}')""".format_map(item))

# =============================== QUERIES =======================================

#armor dump all
#weapon dump all
#build total defence 
#buld total resistance
#build attribute sums

def getArmorStats(armorId):
    result = session.execute(PREPARED_QUERIES['ARMOR_ALL'], [armorId])[0]
    skills = []
    for row in session.execute(PREPARED_QUERIES['BUILD_SKILLS'], [[armorId]]):
        skills.append(row)
    result['skills'] = skills
    return result


def getWeaponStats(weaponId):
    return session.execute(PREPARED_QUERIES['WEAPON_ALL'], [weaponId])[0]

def getBuildDefense(build):
    return session.execute(PREPARED_QUERIES['BUILD_TOTAL_DEFENSE'], [__getIDList(build)])[0]['system.sum(defense_max)']

def getBuildResistances(build):
    return session.execute(PREPARED_QUERIES['BUILD_TOTAL_RESISTANCE'], [__getIDList(build)])[0]

def getBuildSkills(build):
    skills = {}
    for row in session.execute(PREPARED_QUERIES['BUILD_SKILLS'], [__getIDList(build)]):
        skills[row['name']] = skills.get(row['name'], 0) + row['value']
    return skills
            
def __getIDList(build):
    ids = []
    for (_, id) in build.items():
        ids.append(id)
    return ids



