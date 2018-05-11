#!/usr/bin/env python
import neo4j
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://433-06.csse.rose-hulman.edu:7688",auth=basic_auth("neo4j","huntallthemonsters247"))
session = driver.session()

def connect():
    driver = GraphDatabase.driver("bolt://433-06.csse.rose-hulman.edu:7688",auth=basic_auth("neo4j","huntallthemonsters247"))
    session = driver.session()
    return session

def get_skills_by_attribute(attr):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            Skills = tx.run("Match (:Attribute{Name:$name})-[:UNLOCKS]->(s:Skill)"
                "Return distinct s", name = attr)

            i = 0
            for skill in Skills:
                print(skill[0].properties)

def get_skills_by_attribute_amount(attr, amount):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            Skill = tx.run("Match (:Attribute{Name:$name})-[:UNLOCKS]->(s:Skill {Skill_Req:$amount})"
                    "Return distinct s", name = attr, amount = str(amount))
            for obj in Skill:
                print(obj[0].properties)

def get_armor_by_attribute(attribute):
     with driver.session() as session:
        with session.begin_transaction() as tx:
            Armors = tx.run("Match (armor:Armor)-[i:Increases]-(a:Attribute {Name: $attribute})"
                        "Return armor", attribute = attribute)
            for obj in Armors:
                print(obj[0].properties)

def get_armor_by_attribute_inc_only(attribute):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            Armors = tx.run("Match (armor:Armor)-[i:Increases]-(a:Attribute {Name: $attribute})"
                        "Where i.Amount > '0'"
                        "Return armor", attribute = attribute)
            for obj in Armors:
                print(obj[0].properties)

def get_armor_by_attribute_dec_only(attribute):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            Armors = tx.run("Match (armor:Armor)-[i:Increases]-(a:Attribute {Name: $attribute})"
                        "Where i.Amount < '0'"
                        "Return armor", attribute = attribute)
            for obj in Armors:
                print(obj[0].properties)



def add_new_armor(armor):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            tx.run("MERGE (a: Armor {id: $id, Name: $name, Part: $part})"
                    "RETURN a", id = armor['id'], name = armor['Name'], part = armor['Part'])


# HAVING ISSUES WITH THE $AMOUNT IN THE QUERY FOR THE NEXT TWO FUNCTIONS

# def get_armor_by_attribute_greater_than_amount(attribute, amt):
#     with driver.session() as session:
#         with session.begin_transaction() as tx:
#             Armors = tx.run("Match (armor:Armor)-[i:Increases]-(a:Attribute {Name: $attribute})"
#                         "Where i.Amount > $amount"
#                         "Return armor", attribute = attribute, amount = amt)
#             for obj in Armors:
#                 print(obj[0].properties)

# def get_armor_by_attribute_less_than_amount(attribute, amt):
#     with driver.session() as session:
#         with session.begin_transaction() as tx:
#             Armors = tx.run("Match (armor:Armor)-[i:Increases]-(a:Attribute {Name: $attribute})"
#                         "Where i.Amount < $amount"
#                         "Return armor", attribute = attribute, amount = amt)
#             for obj in Armors:
#                 print(obj[0].properties)


# get_skills_by_attribute("Heat Res")
# get_skills_by_attribute_amount("Heat Res", 10)
# get_armor_by_attribute('Mounting')
# get_armor_by_attribute_inc_only('Mounting')
# get_armor_by_attribute_dec_only('Mounting')
# get_armor_by_attribute_greater_than_amount('Mounting', 2)
# get_armor_by_attribute_less_than_amount('Mounting', -1)





#Match (aH:Armor {Part:'Head'})-[iHead:Increases]-(a:Attribute {Name: 'Fire Atk'}) Match (aC:Armor {Part:'Chest'})-[iChest:Increases]-(a) Match (aW:Armor {Part:'Waist'})-[iWaist:Increases]-(a) Match (aL:Armor {Part:'Legs'})-[iLegs:Increases]-(a) Match (aA:Armor {Part:'Arms'})-[iArms:Increases]-(a) Where toInteger(iHead.Amount) + toInteger(iArms.Amount)  + toInteger(iWaist.Amount) + toInteger(iChest.Amount) + toInteger(iLegs.Amount) > 20 return aH, aC, aW, aL, aA, a