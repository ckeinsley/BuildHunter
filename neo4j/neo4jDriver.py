import neo4j
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://433-06.csse.rose-hulman.edu:7688",auth=basic_auth("neo4j","huntallthemonsters247"))
session = driver.session()

def get_skills_by_attribute(attr):
    with driver.session() as session:
        with session.begin_transaction() as tx:
            Skills = tx.run("Match (:Attribute{Name:$name})-[:UNLOCKS]->(s:Skill)"
                "Return distinct s", name = attr)
            #print(Skills[0])
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

get_skills_by_attribute("Heat Res")
get_skills_by_attribute_amount("Heat Res", 10)
get_armor_by_attribute('Mounting')
get_armor_by_attribute_inc_only('Mounting')
get_armor_by_attribute_dec_only('Mounting')