import redis
import pickle
import sys

sys.path.insert(0, '../WebScrapper')

from obj_loader import read_armor_files
from obj_loader import read_decoration_file

_r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=1, password='huntallthemonsters247')

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

def import_decoration_info():
    decoration_list = read_decoration_file()
    for dec in decoration_list:
        id = str(dec.get('id'))
        _r.hset('decoration:' + id, 'rarity', dec.get('Rarity'))
        _r.hset('decoration:' + id, 'carry', dec.get('Carry'))
        _r.hset('decoration:' + id, 'buy', dec.get('Buy'))
        _r.hset('decoration:' + id, 'sell', dec.get('Sell'))
        k = 0
        for var in dec.get('Variations'):
            _r.rpush('decoration:' + id + ':variances', 'decoration:' + id + ':variances:' + str(k))
            _r.hset('decoration:' + id + ':variances:' + str(k), 'craft_price', var.get('Craft_Price'))
            _r.hset('decoration:' + id + ':variances:' + str(k), 'slot', var.get('Slot'))
            m = 0
            for skill in var.get('Skills'):
                _r.rpush('decoration:' + id + ':variances:' + str(k) + ':skills', 'decoration:' + id + ':variances:skills:' + str(m))
                _r.hset('decoration:' + id + ':variances:' + str(k) + ':skills:' + str(m), 'id', skill.get('id'))
                _r.hset('decoration:' + id + ':variances:' + str(k) + ':skills:' + str(m), 'value', skill.get('Value'))
                m += 1
            n = 0
            for item in var.get('Items'):
                _r.rpush('decoration:' + id + ':variances:' + str(k) + ':items', 'decoration:' + id + ':variances:items:' + str(n))
                _r.hset('decoration:' + id + ':variances:' + str(k) + ':items:' + str(n), 'id', item.get('id'))
                _r.hset('decoration:' + id + ':variances:' + str(k) + ':items:' + str(n), 'quantity', item.get('Quantity'))
            k += 1
    print('Import Complete')
        
import_decoration_info()
        