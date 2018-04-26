#!/usr/bin/env python
'''
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

# Standard Imports
import sys

# Object Loader
sys.path.insert(0,'../WebScrapper')
from obj_loader import read_armor_files

# Cassandra Driver
KEYSPACE = 'testkeyspace'

def main():
    (armor_item_list, id_list) = read_armor_files()
    for data in armor_item_list:
        print(data)



if __name__ == "__main__":
    main()