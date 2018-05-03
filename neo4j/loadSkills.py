from neo4j.v1 import GraphDatabase

uri = "bolt://localhost:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "Password"))


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

get_skills_by_attribute("Heat Res")
get_skills_by_attribute_amount("Heat Res", 10)
