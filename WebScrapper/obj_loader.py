import pickle
import bson

ARMORS_PATH = '../WebScrapper/obj/armors/'
WEAPONS_PATH = '../WebScrapper/obj/weapons/'
MONSTERS_PATH = './obj/monsters/'
DECORATIONS_PATH = './obj/decorations/'
SKILLS_PATH = './obj/skills/'
ITEMS_PATH = './obj/items/'

def read_armor_files():
    id_file = open(ARMORS_PATH + 'id_list.p', 'rb')
    id_list = pickle.load(id_file, encoding='unicode')
    id_file.close()
    armor_item_list = []
    for item in id_list:
        item_file = open(ARMORS_PATH + str(item) + '.p', 'rb')
        armor_item_list.append(pickle.load(item_file, encoding='unicode'))
        item_file.close()
    # for i in armor_item_list:
    #     print(i)
    return (armor_item_list, id_list)

def read_skills_file():
    id_file = open(SKILLS_PATH + 'id_list.p', 'rb')
    id_list = pickle.load(id_file, encoding='unicode')
    id_file.close()
    skill_list = []
    for skill in id_list:
        skill_file = open(SKILLS_PATH + str(skill) + '.p', 'rb')
        skill_list.append(pickle.load(skill_file, encoding='unicode'))
        skill_file.close()
    for i in skill_list:
        print(i)
    return (skill_list, id_list)

def read_name_id_mapping():
    f = open('./obj/name_id_map.p', 'rb')
    name_id_mapping = pickle.load(f, encoding='unicode')
    f.close()
    return name_id_mapping

def read_items_file():
    id_file = open(ITEMS_PATH + 'id_dict.bson', 'rb')
    id_dict = id_file.read()
    id_dict = bson.loads(id_dict)
    id_file.close()
    item_list = []
    for item in id_dict['ids']:
        item_file = open(ITEMS_PATH + str(item) + '.bson', 'rb')
        item_list.append(bson.loads(item_file.read()))
        item_file.close()
    return item_list

def read_weapon_file():
    id_file = open(WEAPONS_PATH + 'id_dict.bson', 'rb')
    weapon_dict = id_file.read()
    weapon_dict = bson.loads(weapon_dict)
    id_file.close()
    return weapon_dict

def read_decoration_file():
    id_file = open(DECORATIONS_PATH + 'id_dict.bson', 'rb')
    id_dict = id_file.read()
    id_dict = bson.loads(id_dict)
    id_file.close()
    decorations_list = []
    for dec in id_dict['ids']:
        dec_file = open(DECORATIONS_PATH + str(dec) + '.bson', 'rb')
        decorations_list.append(bson.loads(dec_file.read()))
        dec_file.close()
    return decorations_list