import pickle

ARMORS_PATH = '../WebScrapper/obj/armors/'
WEAPONS_PATH = './obj/weapons/'
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