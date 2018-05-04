import redis
import pickle
import sys

sys.path.insert(0, '../WebScrapper')

from obj_loader import read_armor_files

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

def import_armor_types():
    (armors, ids) = read_armor_files()
    del ids
    for armor in armors:
        _r.sadd('armor:' + armor.get('Part').lower(), armor.get('id'))  

