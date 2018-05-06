#!/usr/bin/env python

from kafka import KafkaProducer
import json

topic = "armor-insert"
armorToInsert = {'Crafting Items': [{'Quantity': '2', 'Name': 'Bnahabra Shell', 'id': 364}, {'Quantity': '3', 'Name': 'Bnahabra Wing', 'id': 366}, {'Quantity': '1', 'Name': 'Thunderbug', 'id': 262}, {'Quantity': '2', 'Name': 'Glueglopper', 'id': 263}], 'Ice': '0', 'Type': 'All', 'Part': 'Head', 'Rarity': '2', 'Thunder': '3', 'Dragon': '3', 'Slot': 0, 'Gender': 'Both', 'Fire': '-3', 'Skills': [{'Value': '-2', 'Name': 'Attack', 'id': 7460}, {'Value': '3', 'Name': 'Status', 'id': 7477}, {'Value': '2', 'Name': 'Sheathing', 'id': 7481}, {'Value': '2', 'Name': 'Paralysis', 'id': 7548}], 'Defense': {'max': '73', 'initial': '5'}, 'Name': 'Bnahabra Headpiece', 'Water': '0', 'Price': '1,400z', 'id': 1923}


def main():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')
    producer.send('my-topic', json.dumps(armorToInsert))
    producer.close()

if __name__ == "__main__":
    main()