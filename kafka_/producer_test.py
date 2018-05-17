#!/usr/bin/env python

from kafka import KafkaProducer
import json
from pprint import pprint

topic = "armor-insert"
armorToInsert = {'Crafting Items': [{'Quantity': '2', 'Name': 'Bnahabra Shell', 'id': 364}, {'Quantity': '3', 'Name': 'Bnahabra Wing', 'id': 366}, {'Quantity': '1', 'Name': 'Thunderbug', 'id': 262}, {'Quantity': '2', 'Name': 'Glueglopper', 'id': 263}], 'Ice': '0', 'Type': 'All', 'Part': 'Head', 'Rarity': '2', 'Thunder': '3', 'Dragon': '3', 'Slot': 0, 'Gender': 'Both', 'Fire': '-3', 'Skills': [{'Value': '-2', 'Name': 'Attack', 'id': 7460}, {'Value': '3', 'Name': 'Status', 'id': 7477}, {'Value': '2', 'Name': 'Sheathing', 'id': 7481}, {'Value': '2', 'Name': 'Paralysis', 'id': 7548}], 'Defense': {'max': '73', 'initial': '5'}, 'Name': 'Bnahabra Headpiece', 'Water': '0', 'Price': '1,400z', 'id': 1923}
weaponToInsert =  {'Affinity': None,
                    'Attack': '288',
                    'Create_Items': [{'Name': 'Iron Ore', 'Quantity': '3', 'id': 202}],
                    'Create_Price': '750z',
                    'Defense': None,
                    'Element': None,
                    'Glaive_Type': None,
                    'Name': 'Iron Sword',
                    'Phial': None,
                    'Rarity': '1',
                    'Shelling': None,
                    'Slot': 0,
                    'True_Attack': '60',
                    'Upgrade_Items': [],
                    'Upgrade_Price': None,
                    'Upgrades_To': [{'Name': 'Iron Sword+', 'id': 5001}],
                    'Weapon_Family': 'Great Sword',
                    'id': 5000}


def main():
    producer = KafkaProducer(bootstrap_servers='433-05.csse.rose-hulman.edu:9092')
    producer.send('insert_weapon', json.dumps(weaponToInsert).encode())
    producer.close()
    print('Added new weapon')

def add_build(user, build_id):
    producer = KafkaProducer(bootstrap_servers='433-05.csse.rose-hulman.edu:9092')
    add_build_msg = {'user' : user, 'build_id' : build_id}
    producer.send('add-build', json.dumps(add_build_msg).encode())
    producer.close()

if __name__ == "__main__":
    #add_build('moorect', 'moorect:Test2')
    main()