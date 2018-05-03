import neo4j
from neo4j.v1 import GraphDatabase, basic_auth

driver = GraphDatabase.driver("bolt://433-06.csse.rose-hulman.edu:7688",auth=basic_auth("neo4j","huntallthemonsters247"))
session = driver.session()

result = session.run('match (n) return n')
print(result)
