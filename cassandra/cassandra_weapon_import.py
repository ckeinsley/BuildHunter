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
    pprint(blademaster_list[10])



    # for weapon in blademaster_list:
    #     print("Processing " + weapon.get('Name'))
    #     if "dummy" in weapon.get('Name'):
    #         continue
        
    print("Finished Dumping Files")


"""
{'Weapon_Family': 'Great Sword', 
    'Element': None, 
    'Slot': 0, 
    'Create_Price': '750z', 
    'Upgrade_Price': None, 
    'id': 5000, 
    'Upgrade_Items': [], 
    'Attack': '288', 
    'Rarity': '1', 
    'Defense': None, 
    'Affinity': None, 
    'True_Attack': '60', 
    'Glaive_Type': None, 
    'Phial': None, 
    'Name': 'Iron Sword', 
    'Upgrades_To': [{'Name': 'Iron Sword+', 'id': 5001}], 
    'Shelling': None, 
    'Create_Items': [{'Name': 'Iron Ore', 'Quantity': '3', 'id': 202}]}
"""


if __name__ == "__main__":
    main()