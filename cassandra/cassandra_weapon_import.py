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
    # print("Connecting to Cassandra")
    # db.connect()
    # print("Connected")
    print("Attempting to create Weapon Table")
    # db.createArmorTable()
    print("Begining Load")
    weapon_list = read_weapon_file()
    print("Load Complete")
    print(weapon_list.get('Blademaster')[0])
    # for armor in weapon_list:
    #     print("Processing armor piece " + armor.get('Name'))
    #     if "dummy" in armor.get('Name'):
    #         continue
    #     db.insertArmor(main_armor, skills, crafting)
    # print("Finished Dumping Files")

if __name__ == "__main__":
    main()