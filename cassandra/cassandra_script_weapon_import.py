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

    for weapon in blademaster_list:
        print("Processing " + weapon.get('Name'))
        pprint(weapon)
        return
        if "dummy" in weapon.get('Name'):
            continue
        db.insertWeapon(weapon)


    print("Dumping Gunner Items")
    gunner_list = weapon_list.get('Gunner')
    for weapon in gunner_list:
        print("Processing " + weapon.get('Name'))
        if "dummy" in weapon.get('Name'):
            continue
        db.insertWeapon(weapon)
        
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


if __name__ == "__main__":
    main()