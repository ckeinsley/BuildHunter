import redis
import pickle
import sys

sys.path.insert(0, '../BuildHunter/')
sys.path.insert(0, '../WebScrapper/')

from obj_loader import read_armor_files
from obj_loader import read_decoration_file
from obj_loader import read_items_file
from obj_loader import read_name_id_mapping

_r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')

def import_data(filename):
    file = open(filename, 'rb')
    data = pickle.load(file, encoding='unicode')
    types = ['armor', 'weapon', 'skill', 'item', 'decoration']
    for key, value in data.items():
        for type_ in types:
            if key.startswith(type_.upper()):
                _r.hset(type_+'_ids', value, key.partition(':')[2])
                _r.hset(type_+'_names', key.partition(':')[2], value)

def import_data_without_filename():
    data = read_name_id_mapping()
    types = ['armor', 'weapon', 'skill', 'item', 'decoration']
    for key, value in data.items():
        for type_ in types:
            if key.startswith(type_.upper()):
                _r.hset(type_+'_ids', value, key.partition(':')[2])
                _r.hset(type_+'_names', key.partition(':')[2], value)

def import_armor_types():
    (armors, ids) = read_armor_files()
    del ids
    for armor in armors:
        _r.sadd('armor:' + armor.get('Part').lower(), armor.get('id'))

def import_decoration_info():
    decoration_list = read_decoration_file()
    for dec in decoration_list:
        id = str(dec.get('id'))
        _r.hset('decoration:' + id, 'name', dec.get('Name'))
        _r.hset('decoration:' + id, 'rarity', dec.get('Rarity'))
        _r.hset('decoration:' + id, 'carry', dec.get('Carry'))
        _r.hset('decoration:' + id, 'buy', dec.get('Buy'))
        _r.hset('decoration:' + id, 'sell', dec.get('Sell'))
        _r.hset('decoration:' + id, 'slot', dec.get('Slots'))
        _r.hset('decoration:' + id, 'craft_price', dec.get('Craft_Price'))
        m = 0
        for skill in dec.get('Skills'):
            _r.sadd('decoration:' + id + ':skills', 'decoration:' + id + ':skills:' + str(m))
            _r.hset('decoration:' + id + ':skills:' + str(m), 'id', skill.get('id'))
            _r.hset('decoration:' + id + ':skills:' + str(m), 'name', skill.get('Name'))
            _r.hset('decoration:' + id + ':skills:' + str(m), 'value', skill.get('Value'))
            m += 1
        n = 0
        for recipe in dec.get('Recipes'):
            _r.sadd('decoration:' + id + ':recipes', 'decoration:' + id + ':recipe:' + str(n))
            p = 0
            for item in recipe:
                _r.sadd('decoration:' + id + ':recipe:' + str(n), 'decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p))
                _r.hset('decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p), 'id', item.get('id'))
                _r.hset('decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p), 'name', item.get('Name'))
                _r.hset('decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p), 'quantity', item.get('Quantity'))
                p += 1
            n += 1
    print('Import Complete')

def import_item_info():
    item_list = read_items_file()
    for item in item_list:
        id = str(item.get('id'))
        _r.hset('item:' + id, 'name', item.get('Name'))
        _r.hset('item:' + id, 'rarity', item.get('Rarity'))
        _r.hset('item:' + id, 'carry', item.get('Carry'))
        _r.hset('item:' + id, 'buy', item.get('Buy'))
        _r.hset('item:' + id, 'sell', item.get('Sell'))
        k = 0
        for combo in item.get('Combo_List'):
            _r.sadd('item:' + id + ':combo_list', 'item:' + id + ':combo_list:' + str(k))
            _r.hset('item:' + id + ':combo_list:' + str(k), 'id_1', combo.get('id_1'))
            _r.hset('item:' + id + ':combo_list:' + str(k), 'name_1', combo.get('Name_1'))
            _r.hset('item:' + id + ':combo_list:' + str(k), 'id_2', combo.get('id_2'))
            _r.hset('item:' + id + ':combo_list:' + str(k), 'name_2', combo.get('Name_2'))
        m = 0
        for loc in item.get('Gather_Locations'):
            _r.sadd('item:' + id + ':gather_locations', 'item:' + id + ':gather_locations:' + str(m))
            _r.hset('item:' + id + ':gather_locations:' + str(m), 'rank', loc.get('Rank'))
            _r.hset('item:' + id + ':gather_locations:' + str(m), 'map', loc.get('Map'))
            _r.hset('item:' + id + ':gather_locations:' + str(m), 'area', loc.get('Area'))
            _r.hset('item:' + id + ':gather_locations:' + str(m), 'gather_method', loc.get('Gather_Method'))
            _r.hset('item:' + id + ':gather_locations:' + str(m), 'quantity', loc.get('Quantity'))
            _r.hset('item:' + id + ':gather_locations:' + str(m), 'drop_rate', loc.get('Drop_Rate'))

import_data_without_filename()
import_armor_types()
import_decoration_info()
import_item_info()