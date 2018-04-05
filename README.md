# BuildHunter

## Team
- Christopher Keinsley
- Collin Moore
- Rahul Yarlagadda

## Features
- Query for Individual Items
    - Includes information about
        - Drop rate
        - Gather locations
        - Which mosters drop them
- Search for Monsters
    - Retrieve information about monsters such as 
        - Weaknesses
        - Damage required for part break
- Look up Equipment and Gear (Weapons/Armor)
    - Will include
        - Attribute points obtained by wearing the gear
        - Available slots in the gear
        - Items required to craft
- Load / Store: Custom Gear Loadouts
    - Each loadout can be saved by an individual
    - Each loadout can be published 
    - Generates the materials required for crafting
    - Allows customization of decorations
    - Generates a list of skills obtained by the loadout
- Search published loadouts
    - Load published loadouts, change, and save them
- Query skills
    - Show how many and which attribute points are required to obtain a skill

## Tools

**Streaming Service**
- Kafka
    - Pub Sub service for writing to databases


**Databases**  
- Kasandra
    - Store Equipment and Weapons
    ![](images/Cassandra.png)
- Neo4j
    - For build generation and skill querying
    ![](images/neo4j_datastructure.png)
- Redis
    - Crafting and Consumable items
    - User made builds
    - Query builds
    ![](images/redis_diagram.png)
## Reach Goals
- Generate builds per skills desired

## Notes on Running
- How to start neo4j
    - sudo service neo4j {start|stop|restart}
- Install cqlsh
    - Make sure to use pip, not pip3; python 2.7 not python 3.x.
    - pip install cqlsh
    - pip install cassandra-driver
    - export CQLSH_NO_BUNDLED=true
    - echo ‘export CQLSH_NO_BUNDLED=true’ >> ~/.bashrc
    - cqlsh –cqlversion=3.4.4
