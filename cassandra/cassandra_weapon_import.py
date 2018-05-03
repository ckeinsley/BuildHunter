#!/usr/bin/env python
# Standard Imports
import sys
from pprint import pprint

# Object Loader
sys.path.insert(0,'../WebScrapper')
from obj_loader import read_weapon_file

# Cassandra Driver
import cassandraDriver as db
KEYSPACE = 'testkeyspace'

def main():
    print("Connecting to Cassandra")
    db.connect()
    print("Connected")
    db.createWeaponTable()
    print("Begining Load")
    weapon_list = read_weapon_file()
    print("Load Complete")
    
    print("Dumping blademaster Items")
    blademaster_list = weapon_list.get('Blademaster')
    weapon = blademaster_list[0]

    weaponToInsert = parseWeapon(weapon, True)
    createItems = parseCreateItems(weapon)
    upgradeItems = parseUpgradeItems(weapon)
    upgradesTo = parseUpgradesTo(weapon)

    db.insertWeapon(weaponToInsert,createItems,upgradeItems,upgradesTo)

    # for weapon in blademaster_list:
    #     print("Processing " + weapon.get('Name'))
    #     if "dummy" in weapon.get('Name'):
    #         continue
    #     weaponToInsert = parseWeapon(weapon, True)
    #     createItems = parseCreateItems(weapon)
    #     upgradeItems = parseUpgradeItems(weapon)
    #     upgradesTo = parseUpgradesTo(weapon)

    # print("Dumping Gunner Items")
    # gunner_list = weapon_list.get('Gunner')
    # for weapon in gunner_list:
    #     print("Processing " + weapon.get('Name'))
    #     if "dummy" in weapon.get('Name'):
    #         continue
    #     weaponToInsert = parseWeapon(weapon, True)
    #     createItems = parseCreateItems(weapon)
    #     upgradeItems = parseUpgradeItems(weapon)
    #     upgradesTo = parseUpgradesTo(weapon)
        
    print("Finished Dumping Files")


"""
{'Affinity': '15',
 'Attack': '720',
 'Create_Items': [],
 'Create_Price': None,
 'Defense': None,
 'Element': {'Name': ' Poison ', 'Value': ' 300 '},
 'Glaive_Type': None,
 'Name': 'Chrome Razor',
 'Phial': None,
 'Rarity': '4',
 'Shelling': None,
 'Slot': 1,
 'True_Attack': '150',
 'Upgrade_Items': [{'Name': 'G.Jaggi Claw+', 'Quantity': '3', 'id': 390},
                   {'Name': 'Carbalite Ore', 'Quantity': '2', 'id': 212},
                   {'Name': 'Toxin Sac', 'Quantity': '3', 'id': 332},
                   {'Name': 'Bird Wyvern Gem', 'Quantity': '1', 'id': 324}],
 'Upgrade_Price': '20,000z',
 'Upgrades_To': [{'Name': 'Chrome Quietus', 'id': 5011}],
 'Weapon_Family': 'Great Sword',
 'id': 5010}
"""

def parseWeapon(weapon, blademaster):
    newWeapon = {}
    newWeapon['affinity'] = intOrNone(weapon.get('Affinity'))
    newWeapon['attack'] = intOrNone(weapon.get('Attack'))
    newWeapon['create_price'] = weapon.get('Create_Price').replace("'", "''")
    newWeapon['defense'] = intOrNone(weapon.get('Defense'))
    newWeapon['glaive_type'] = weapon.get('Glaive_Type').replace("'", "''")
    newWeapon['name'] = weapon.get('Name').replace("'", "''")
    newWeapon['phial'] = weapon.get('Phial').replace("'", "''")
    newWeapon['rarity'] = intOrNone('Rarity')
    newWeapon['shelling'] = weapon.get('Shelling').replace("'", "''")
    newWeapon['slot'] = intOrNone(weapon.get('Slot'))
    newWeapon['true_attack'] = intOrNone(weapon.get('True_Attack'))
    newWeapon['upgrade_price'] = weapon.get('Upgrade_Price').replace("'", "''")
    newWeapon['weapon_family'] = weapon.get('Weapon_Family').replace("'", "''")
    newWeapon['id'] = intOrNone(weapon.get('id'))
    if blademaster:
        newWeapon['class'] = 'Blademaster'
    else:
        newWeapon['class'] = 'Gunner'
    return newWeapon

def parseCreateItems(weapon):
    items = []
    wep_id = intOrNone(weapon.get('id'))
    for create_item in weapon.get('Create_Items'):
        item_map = {}
        item_map['id'] = wep_id
        item_map['name'] = create_item['Name'].replace("'", "''")
        item_map['quantity'] = intOrNone(create_item['Quantity'])
        item_map['item_id'] = intOrNone(create_item['id'])
        items.append(item_map)
    return items

def parseUpgradeItems(weapon):
    items = []
    wep_id = intOrNone(weapon.get('id'))
    for upgrade_item in weapon.get('Upgrade_Items'):
        item_map = {}
        item_map['id'] = wep_id
        item_map['name'] = upgrade_item['Name'].replace("'", "''")
        item_map['quantity'] = intOrNone(upgrade_item['Quantity'])
        item_map['item_id'] = intOrNone(upgrade_item['id'])
        items.append(item_map)
    return items

def parseUpgradesTo(weapon):
    items = []
    wep_id = intOrNone(weapon.get('id'))
    for upgrade_item in weapon.get('Upgrades_To'):
        item_map = {}
        item_map['id'] = wep_id
        item_map['name'] = upgrade_item['Name'].replace("'", "''")
        item_map['item_id'] = intOrNone(upgrade_item['id'])
        items.append(item_map)
    return items

def intOrNone(possibleInt):
    try:
        return int(possibleInt)
    except:
        return None

if __name__ == "__main__":
    main()