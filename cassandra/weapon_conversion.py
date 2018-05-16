def convertWeapon(weapon):
    blademaster = __isBlademaster(weapon)
    newWeapon = {}
    newWeapon['affinity'] = __intOrNone(weapon.get('Affinity'))
    newWeapon['attack'] = __intOrNone(weapon.get('Attack'))
    newWeapon['create_price'] = __filterString(weapon.get('Create_Price'))
    newWeapon['defense'] = __intOrNone(weapon.get('Defense'))
    newWeapon['glaive_type'] = __filterString(weapon.get('Glaive_Type'))
    newWeapon['name'] = __filterString(weapon.get('Name'))
    newWeapon['phial'] = __filterString(weapon.get('Phial'))
    newWeapon['rarity'] = __intOrNone('Rarity')
    newWeapon['shelling'] = __filterString(weapon.get('Shelling'))
    newWeapon['slot'] = __intOrNone(weapon.get('Slot'))
    newWeapon['true_attack'] = __intOrNone(weapon.get('True_Attack'))
    newWeapon['upgrade_price'] = __filterString(weapon.get('Upgrade_Price'))
    newWeapon['weapon_family'] = __filterString(weapon.get('Weapon_Family'))
    newWeapon['id'] = __intOrNone(weapon.get('id'))
    if blademaster:
        newWeapon['class'] = 'Blademaster'
    else:
        newWeapon['class'] = 'Gunner'
    return newWeapon 

def __isBlademaster(weapon):
    weapon_family = weapon.get('Weapon_Family')
    gun = ["Bow","Light Bowgun", "Heavy Bowgun"]
    return not weapon_family in gun

def convertCreateItems(weapon):
    print(weapon)
    items = []
    wep_id = __intOrNone(weapon.get('id'))
    for create_item in weapon.get('Create_Items'):
        item_map = {}
        item_map['id'] = wep_id
        item_map['name'] = __filterString(create_item['Name'])
        item_map['quantity'] = __intOrNone(create_item['Quantity'])
        item_map['item_id'] = __intOrNone(create_item['id'])
        items.append(item_map)
    return items

def convertUpgradeItems(weapon):
    items = []
    wep_id = __intOrNone(weapon.get('id'))
    for upgrade_item in weapon.get('Upgrade_Items'):
        item_map = {}
        item_map['id'] = wep_id
        item_map['name'] = __filterString(upgrade_item['Name'])
        item_map['quantity'] = __intOrNone(upgrade_item['Quantity'])
        item_map['item_id'] = __intOrNone(upgrade_item['id'])
        items.append(item_map)
    return items

def convertUpgradesTo(weapon):
    items = []
    wep_id = __intOrNone(weapon.get('id'))
    for upgrade_item in weapon.get('Upgrades_To'):
        item_map = {}
        item_map['id'] = wep_id
        item_map['name'] = __filterString(upgrade_item['Name'])
        item_map['item_id'] = __intOrNone(upgrade_item['id'])
        items.append(item_map)
    return items


def __filterString(someString):
    if someString:
        return someString.replace("'", "''")
    else:
        return None

def __intOrNone(possibleInt):
    try:
        return int(possibleInt)
    except:
        return -1