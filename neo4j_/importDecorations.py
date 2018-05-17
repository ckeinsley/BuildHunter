#!/usr/bin/env python
# Standard Imports
import sys
from pprint import pprint

from neo4j.v1 import GraphDatabase

# Object Loader
sys.path.insert(0,'../WebScrapper')
from obj_loader import read_armor_files


uri = "bolt://433-06.csse.rose-hulman.edu:7688"
driver = GraphDatabase.driver(uri, auth=("neo4j", "huntallthemonsters247"))
allDecoration = read_armor_files()

#allArmor[0][0]['Skills'][0]['Description'] = 'None'

def add_decoration():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for decoration in allDecoration[0]:
                tx.run("MERGE (a: Decoration {id: $id, Name: $name, Part: $part})"
                        "RETURN a", id = decoration['id'], name = decoration['Name'], part = decoration['Part'])
                
                #for skill in attribute['Skills']:
                    #print(skill)
                #    tx.run("MERGE (s: Skill {Name: $name, Skill_Req: $Skill_Req, Description: $Description})"
                #        "RETURN s", name = skill['Name'], Skill_Req = skill['Skill_Req'], Description = skill['Description'])
        session.close()


def add_armor_relations():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for decoration in allDecoration[0]:
                for skill in decortaion['Skills']:
                    tx.run("MATCH (skill:Attribute {Name: $name})"
                            "MATCH (armor:Armor {Name: $armorName})"
                            "CREATE UNIQUE (armor)-[boost:Increases {Amount: $Amount}]->(skill)", name = skill['Name'], armorName = armor['Name'], Amount = skill['Value'])
add_decoration()
add_decoration_relations()