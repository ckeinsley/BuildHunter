#!/usr/bin/env python
# Standard Imports
import sys
from pprint import pprint

# Object Loader
sys.path.insert(0,'../WebScrapper')
from obj_loader import read_armor_files

# Cassandra Driver
import cassandraDriver as db
KEYSPACE = 'testkeyspace'

def main():
    print("Connecting to Cassandra")
    db.connect()
    print("Connected")
    print("Attempting to create Armor Table")
    db.createArmorTable()
    print("Begining Load")
    (armor_item_list, id_list) = read_armor_files()
    print("Load Complete")
    # for armor in armor_item_list:
    armor = convertArmor(armor_item_list[0])
    db.insertArmor(armor)
    pprint(armor)
    print("Processing armor piece " + armor.get('name'))
    # db.insertArmor(armor)
    print("Finished Dumping Files")

'''
Loaded Format
----------------------------------
Armor_Item:
    {
        'id' : '1248329814',
        Name : 'Leather Trousers',
        Type : 'All',
        Part : 'Head',
        Gender : 'Both',
        Rarity : '1',
        Defense : {
            'initial' : '1',
            'max' : '71'
        }
        Slot : '1',
        Fire : '-1',
        Water : '0',
        Ice : '0',
        Thunder : '0',
        Dragon : '1',
        Skills : [
            {
                'id' : '1234125',
                'Name' : 'Gathering',
                'Value' : '1'
            },
            {
                'id' : '12314850',
                'Name' : 'Whim',
                'Value' : '3'
            }
        ],
        'Crafting Items' : [
            {
                'id' : '11235143',
                'Name' : 'Warm Pelt' 
                'Quantity': '1'
            },
            {
                'id' : '12341542323',
                'Name' : 'Iron Ore',
                'Quanity' : '1'
            }
        ]
    }
'''
def convertArmor(armor):
    convertedArmor = {}
    convertedArmor['name'] = armor.get('Name')
    convertedArmor['id'] = int(armor.get('id'))
    convertedArmor['price'] = armor.get('Price')
    convertedArmor['part'] = armor.get('Part')
    convertedArmor['rarity']= int(armor.get('Rarity'))
    convertedArmor['slot'] = int(armor.get('Slot'))
    convertedArmor['type'] = armor.get('Type')
    convertedArmor['gender'] = armor.get('Gender')
    convertedArmor['skill'] = armor.get('Skills')
    convertedArmor['crafting_item'] = armor.get('Crafting Items')
    convertedArmor['defense'] = convertDefense(armor.get('Defense'))
    convertedArmor['resist'] = convertResistances(armor)
    return convertedArmor

def convertDefense(defense):
    initial = int(defense.get('initial'))
    maximum = int(defense.get('max'))
    defenseDict = {}
    defenseDict['max'] = maximum
    defenseDict['initial'] = initial
    return defenseDict

def convertResistances(armor):
    resist = []
    resist.append({'fire':int(armor.get('Fire'))})
    resist.append({'dragon':int(armor.get('Dragon'))})
    resist.append({'water':int(armor.get('Water'))})
    resist.append({'ice':int(armor.get('Ice'))})
    resist.append({'thunder':int(armor.get('Thunder'))})
    return resist

if __name__ == "__main__":
    main()