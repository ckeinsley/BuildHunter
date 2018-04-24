import redis
import pickle

_r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')

def import_data(filename):
    file = open(filename, 'rb')
    data = pickle.load(file, encoding='unicode')
    types = ['armor', 'weapon', 'skill', 'item']
    for key, value in data.items():
        for type_ in types:
            if key.startswith(type_.upper()):
                _r.hset(type_+'_ids', value, key.partition(':')[2])
                _r.hset(type_+'_names', key.partition(':')[2], value)

