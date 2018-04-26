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
    armor = armor_item_list[0];
    main_armor = convertArmor(armor)
    skills = convertSkills(armor)
    crafting = convertCrafting(armor)

    pprint(main_armor)
    pprint(skills)
    pprint(crafting)

    db.insertArmor(armor, skills, crafting)
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
    extractDefense(convertedArmor, armor)
    extractResistances(convertedArmor, armor)
    return convertedArmor

def extractDefense(armorMap, armor):
    armorMap['defense_init'] = armor.get('Defense').get('initial')
    armorMap['defense_max'] = armor.get('Defense').get('max')

def extractResistances(armorMap, armor):
    armorMap['fire'] = armor.get('Fire')
    armorMap['dragon'] = armor.get('Dragon')
    armorMap['water'] = armor.get('Water')
    armorMap['thunder'] = armor.get('Thunder')
    armorMap['ice'] = armor.get('Ice')

def convertSkills(armor):
    skillsList = []
    for skill in armor.get('Skills'):
        skillmap = {}
        skillmap['id'] = armor.get('id')
        skillmap['skill_id'] = skill.get('id')
        skillmap['name'] = skill.get('Name')
        skillmap['value'] = skill.get('Value')
        skillsList.append(skillmap)
    return skillsList

def convertCrafting(armor):
    craftingList = []
    for item in armor.get('Crafting Items'):
        craftmap = {}
        craftmap['id'] = armor.get('id')
        craftmap['item_id'] = item.get('id')
        craftmap['name'] = item.get('Name')
        craftmap['quantity'] = item.get('Quantity')
    return craftingList

if __name__ == "__main__":
    main()