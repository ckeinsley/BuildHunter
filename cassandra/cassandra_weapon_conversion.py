
def convertArmor(armor):
    convertedArmor = {}
    convertedArmor['id'] = int(armor.get('id'))
    convertedArmor['price'] = armor.get('Price')
    convertedArmor['part'] = armor.get('Part')
    convertedArmor['rarity']= int(armor.get('Rarity'))
    convertedArmor['slot'] = int(armor.get('Slot'))
    convertedArmor['type'] = armor.get('Type')
    convertedArmor['gender'] = armor.get('Gender')
    __extractDefense(convertedArmor, armor)
    __extractResistances(convertedArmor, armor)
    convertedArmor['name'] = armor.get('Name').replace("'","''")
    return convertedArmor

def __extractDefense(armorMap, armor):
    try:
        initial = int(armor.get('Defense').get('initial'))
    except:
        initial = -1
    try:
        maximum = int(armor.get('Defense').get('max'))
    except:
        maximum = -1
    armorMap['defense_init'] = initial
    armorMap['defense_max'] = maximum

def __extractResistances(armorMap, armor):
    armorMap['fire'] = int(armor.get('Fire'))
    armorMap['dragon'] = int(armor.get('Dragon'))
    armorMap['water'] = int(armor.get('Water'))
    armorMap['thunder'] = int(armor.get('Thunder'))
    armorMap['ice'] = int(armor.get('Ice'))

def convertSkills(armor):
    skillsList = []
    for skill in armor.get('Skills'):
        skillmap = {}
        skillmap['id'] = int(armor.get('id'))
        skillmap['skill_id'] = int(skill.get('id'))
        skillmap['name'] = skill.get('Name').replace("'", "''")
        skillmap['value'] = int(skill.get('Value'))
        skillsList.append(skillmap)
    return skillsList

def convertCrafting(armor):
    craftingList = []
    for item in armor.get('Crafting Items'):
        craftmap = {}
        craftmap['id'] = int(armor.get('id'))
        craftmap['item_id'] = int(item.get('id'))
        craftmap['name'] = item.get('Name').replace("'", "''")
        craftmap['quantity'] = int(item.get('Quantity'))
        craftingList.append(craftmap)
    return craftingList