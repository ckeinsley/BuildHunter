import sys
from neo4j.v1 import GraphDatabase

from pprint import pprint

# Object Loader
sys.path.insert(0,'../WebScrapper')
from obj_loader import read_skills_file
uri = "bolt://433-06.csse.rose-hulman.edu:7688"
driver = GraphDatabase.driver(uri, auth=("neo4j", "huntallthemonsters247"))
allSkills = read_skills_file()

allSkills[0][0]['Skills'][0]['Description'] = 'None'

def add_skills():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for attribute in allSkills[0]:
                tx.run("MERGE (a: Attribute {id: $id, Name: $name})"
                        "RETURN a", id = attribute['id'], name = attribute['Name'])
                
                for skill in attribute['Skills']:
                    #print(skill)
                    tx.run("MERGE (s: Skill {Name: $name, Skill_Req: $Skill_Req, Description: $Description})"
                        "RETURN s", name = skill['Name'], Skill_Req = skill['Skill_Req'], Description = skill['Description'])
        session.close()

def add_relations():
    with driver.session() as session:
        with session.begin_transaction() as tx:
            for attribute in allSkills[0]:
                for skill in attribute['Skills']:
                    tx.run("MATCH (attr:Attribute {Name: $name})"
                            "MATCH (newSkill:Skill {Description: $Desc})"
                            "CREATE (attr)-[unlock:UNLOCKS {Skill_Req: $Skill_Req}]->(newSkill)", name = attribute['Name'], Desc = skill['Description'], Skill_Req = skill['Skill_Req'])


                    
#add_skills()
#add_relations()
