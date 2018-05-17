import redis
import sys

def connection_decorator(function):
    def wrapper(*args, **kwargs):
        retVal = None
        try:
            retVal = function(*args, **kwargs)
        except redis.exceptions.ConnectionError:
            if not args[0]._is_master:
                for i in range(5,9):
                    try: 
                        r = redis.StrictRedis(host='433-0' + str(i) + '.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')
                        r.ping() #Will throw exception if connection not
                        print('Reconnected to redis on node ' + str(i))
                        args[0]._r = r
                        return function(*args, **kwargs)
                    except redis.exceptions.ConnectionError:
                        pass
            raise(ConnectionError('Could not connect to redis.'))
        return retVal
    return wrapper

class RedisDriver:

    _r = None
    _is_master = False

    def __init__(self, is_master):
        self._r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')
        self._is_master = is_master

    def ping(self):
        try:
            response = self._r.ping()
            return response
        except Exception as ex:
            print(str(ex))
            return False

    ####----active_user and active_build properties----####
    @connection_decorator
    def is_user(self, user):
        val = self._r.sismember('users', user)
        return val
    
    @connection_decorator
    def build_exists_for_user(self, user, build_id):
        return self._r.sismember(user + ':builds', build_id)

    ####----Users----####
    @connection_decorator
    def add_user(self, user):
        self._r.sadd('users', user)
    
    @connection_decorator
    def delete_user(self, user):
        self._r.delete(*self._r.keys(user + ':*'))
        self._r.srem('users', user)

    ####----Builds----####
    
    @connection_decorator
    def add_build(self, user, buildId):
        #Add build to user builds
        self._r.sadd(user + ":builds", buildId)
    
    @connection_decorator
    def delete_build(self, user, buildId, build_parts):
        #Remove from user build list
        self._r.srem(user + ":builds", buildId)

        #Delete build hash
        self._r.delete(buildId)

        #Delete decoration sets
        for part in build_parts:
            self._r.delete(buildId + ':' + part)
    
    @connection_decorator
    def get_all_builds(self, user):
        return self._r.smembers(user + ':builds')
    
    ####----Build Components (e.g. armor pieces, weapons)----####

    BUILD_PARTS = {'head', 'chest', 'arms', 'waist', 'legs', 'weapon'}
    
    @connection_decorator
    def add_build_component(self, build_id, part, item_id):
        self._r.hset(build_id, part, item_id)

    @connection_decorator
    def remove_build_component(self, build_id, part):
        self._r.hdel(build_id, part)
        self._r.delete(build_id + ':' + part)
    
    @connection_decorator
    def get_build_parts(self, build_id):
        return self._r.hgetall(build_id)

    @connection_decorator
    def is_part(self, id, part):
        if (part == 'weapon'):
            return self.is_object(id, 'weapon')
        return self._r.sismember('armor:' + part, id)
    
    ####----Decorations----####

    @connection_decorator
    def add_decoration(self, build_id, part, itemId):
        self._r.rpush(build_id + ':' + part, itemId)
    
    @connection_decorator
    def remove_decoration(self, build_id, part, itemId):
        self._r.lrem(build_id + ':' + part, 1, itemId)

    @connection_decorator
    def get_decorations(self, build_id, part):
        return self._r.lrange(build_id + ':' + part, 0, -1)

    @connection_decorator
    def remove_all_decorations(self, build_id, part):
        self._r.delete(build_id + ':' + part)

    @connection_decorator
    def is_decoration(self, id):
        return self._r.hexists('decoration_ids', id)

    ####----Items----####

    ITEM_TYPES = {'armor', 'weapon', 'skill', 'item', 'decoration'}

    @connection_decorator
    def get_object_name(self, id, type_):
        return self._r.hget(type_+ '_ids', id)
    
    @connection_decorator
    def search_object_name(self, name, type_):
        return self._r.hscan_iter(type_ + '_names', '*' + name + '*')

    @connection_decorator    
    def get_object_type(self, id):
        for type_ in self.ITEM_TYPES:
            if self._r.hexists(type_ + '_ids', id):
                return type_
        return None
    
    @connection_decorator
    def get_object_id(self, name, type_):
        return self._r.hget(type_+ '_names', name)
    
    @connection_decorator
    def is_object(self, id, type_):
        return self._r.hget(type_+ '_ids', id) is not None

    ####----Armor----####

    """ def add_armor_data(self, armor):
        if self.is_object(int(armor.get('id')), 'armor'):
            self._r.hset('armor:' + str(armor.get('id')), 'name', armor.get('Name'))
            self._r.hset('armor:' + str(armor.get('id')), 'part', armor.get('Part'))
            self._r.hset('armor:' + str(armor.get('id')), 'type', armor.get('Type'))
            self._r.hset('armor:' + str(armor.get('id')), 'slot', armor.get('Slot'))
            n = 0
            for item in armor.get('Crafting Items'):
                self._r.sadd('armor:' + str(armor.get('id')) + ':crafting_items', 'armor:' + str(armor.get('id')) + ':crafting_item:' + str(n))
                self._r.hset('armor:' + str(armor.get('id')) + ':crafting_item:' + str(n), 'id', item.get('id'))
                self._r.hset('armor:' + str(armor.get('id')) + ':crafting_item:' + str(n), 'name', item.get('Name'))
                self._r.hset('armor:' + str(armor.get('id')) + ':crafting_item:' + str(n), 'quantity', item.get('Quantity'))
                n += 1
    
    def get_armor_data(self, id):
        if self.is_object(id, 'armor'):
            armor_dict = {}
            armor_dict['name'] = self._r.hget('armor:' + str(id), 'name').decode('utf-8')
            armor_dict['part'] = self._r.hget('armor:' + str(id), 'part').decode('utf-8')
            armor_dict['type'] = self._r.hget('armor:' + str(id), 'type').decode('utf-8')
            armor_dict['slot'] = self._r.hget('armor:' + str(id), 'slot').decode('utf-8')
            armor_dict['crafting_items'] = []
            crafting_items = self._r.smembers('armor:' + str(id) + ':crafting_items')
            for item in crafting_items:
                temp_item = {}
                temp_item['id'] = self._r.hget(item, 'id').decode('utf-8')
                temp_item['name'] = self._r.hget(item, 'name').decode('utf-8')
                temp_item['quantity'] = self._r.hget(item, 'quantity').decode('utf-8')
                armor_dict['crafting_items'].append(temp_item)
            return armor_dict
        else:
            print('No armor matching id: %s' % str(id))
            return {} """


    ####----Item----####

    @connection_decorator
    def add_item_data(self, item):
        if self.is_object(item.get('id'), 'item'):
            id = str(item.get('id'))
            self._r.hset('item:' + id, 'name', item.get('Name'))
            self._r.hset('item:' + id, 'rarity', item.get('Rarity'))
            self._r.hset('item:' + id, 'carry', item.get('Carry'))
            self._r.hset('item:' + id, 'buy', item.get('Buy'))
            self._r.hset('item:' + id, 'sell', item.get('Sell'))
            k = 0
            for combo in item.get('Combo_List'):
                self._r.sadd('item:' + id + ':combo_list', 'item:' + id + ':combo_list:' + str(k))
                self._r.hset('item:' + id + ':combo_list:' + str(k), 'id_1', combo.get('id_1'))
                self._r.hset('item:' + id + ':combo_list:' + str(k), 'name_1', combo.get('Name_1'))
                self._r.hset('item:' + id + ':combo_list:' + str(k), 'id_2', combo.get('id_2'))
                self._r.hset('item:' + id + ':combo_list:' + str(k), 'name_2', combo.get('Name_2'))
            m = 0
            for loc in item.get('Gather_Locations'):
                self._r.sadd('item:' + id + ':gather_locations', 'item:' + id + ':gather_locations:' + str(m))
                self._r.hset('item:' + id + ':gather_locations:' + str(m), 'rank', loc.get('Rank'))
                self._r.hset('item:' + id + ':gather_locations:' + str(m), 'map', loc.get('Map'))
                self._r.hset('item:' + id + ':gather_locations:' + str(m), 'area', loc.get('Area'))
                self._r.hset('item:' + id + ':gather_locations:' + str(m), 'gather_method', loc.get('Gather_Method'))
                self._r.hset('item:' + id + ':gather_locations:' + str(m), 'quantity', loc.get('Quantity'))
                self._r.hset('item:' + id + ':gather_locations:' + str(m), 'drop_rate', loc.get('Drop_Rate'))
        else:
            print('No item matching id: %s' % str(item.get('id')))

    @connection_decorator
    def get_item_data(self, id):
        if self.is_object(id, 'item'):
            item_dict = {}
            item_dict['name'] = self._r.hget('item:' + str(id), 'name').decode('utf-8')
            item_dict['rarity'] = self._r.hget('item:' + str(id), 'rarity').decode('utf-8')
            item_dict['carry'] = self._r.hget('item:' + str(id), 'carry').decode('utf-8')
            item_dict['buy'] = self._r.hget('item:' + str(id), 'buy').decode('utf-8')
            item_dict['sell'] = self._r.hget('item:' + str(id), 'sell').decode('utf-8')
            item_dict['combo_list'] = []
            item_dict['gather_locations'] = []
            combo_ids = self._r.smembers('item:' + str(id) + ':combo_list')
            for cid in combo_ids:
                temp_combo = {}
                temp_combo['id_1'] = self._r.hget(cid, 'id_1').decode('utf-8')
                temp_combo['name_1'] = self._r.hget(cid, 'name_1').decode('utf-8')
                temp_combo['id_2'] = self._r.hget(cid, 'id_2').decode('utf-8')
                temp_combo['name_2'] = self._r.hget(cid, 'name_2').decode('utf-8')
                item_dict['combo_list'].append(temp_combo)
            gather_loc_ids = self._r.smembers('item:' + str(id) + ':gather_locations')
            for locs in gather_loc_ids:
                temp_loc = {}
                temp_loc['rank'] = self._r.hget(locs, 'rank').decode('utf-8')
                temp_loc['map'] = self._r.hget(locs, 'map').decode('utf-8')
                temp_loc['area'] = self._r.hget(locs, 'area').decode('utf-8')
                temp_loc['gather_method'] = self._r.hget(locs, 'gather_method').decode('utf-8')
                temp_loc['quantity'] = self._r.hget(locs, 'quantity').decode('utf-8')
                temp_loc['drop_rate'] = self._r.hget(locs, 'drop_rate').decode('utf-8')
                item_dict['gather_locations'].append(temp_loc)
            return item_dict
        else:
            print('No item matching id: %s' % str(id))
            return {}

    ####----Decorations----####
    
    @connection_decorator
    def add_decoration_data(self, decoration):
        dec = decoration
        id = str(dec.get('id'))
        self._r.hset('decoration:' + id, 'name', dec.get('Name'))
        self._r.hset('decoration:' + id, 'rarity', dec.get('Rarity'))
        self._r.hset('decoration:' + id, 'carry', dec.get('Carry'))
        self._r.hset('decoration:' + id, 'buy', dec.get('Buy'))
        self._r.hset('decoration:' + id, 'sell', dec.get('Sell'))
        self._r.hset('decoration:' + id, 'slot', dec.get('Slots'))
        self._r.hset('decoration:' + id, 'craft_price', dec.get('Craft_Price'))
        m = 0
        for skill in dec.get('Skills'):
            self._r.sadd('decoration:' + id + ':skills', 'decoration:' + id + ':skills:' + str(m))
            self._r.hset('decoration:' + id + ':skills:' + str(m), 'id', skill.get('id'))
            self._r.hset('decoration:' + id + ':skills:' + str(m), 'name', skill.get('Name'))
            self._r.hset('decoration:' + id + ':skills:' + str(m), 'value', skill.get('Value'))
            m += 1
        n = 0
        for recipe in dec.get('Recipes'):
            self._r.sadd('decoration:' + id + ':recipes', 'decoration:' + id + ':recipe:' + str(n))
            p = 0
            for item in recipe:
                self._r.sadd('decoration:' + id + ':recipe:' + str(n), 'decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p))
                self._r.hset('decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p), 'id', item.get('id'))
                self._r.hset('decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p), 'name', item.get('Name'))
                self._r.hset('decoration:' + id + ':recipe:' + str(n) + ':item:' + str(p), 'quantity', item.get('Quantity'))
                p += 1
            n += 1

    @connection_decorator
    def get_decoration_data(self, id):
        if self.is_object(id, 'decoration'):
            dec_dict = {}
            dec_dict['name'] = self._r.hget('decoration:' + str(id), 'name').decode('utf-8')
            dec_dict['rarity'] = self._r.hget('decoration:' + str(id), 'rarity').decode('utf-8')
            dec_dict['carry'] = self._r.hget('decoration:' + str(id), 'carry').decode('utf-8')
            dec_dict['buy'] = self._r.hget('decoration:' + str(id), 'buy').decode('utf-8')
            dec_dict['sell'] = self._r.hget('decoration:' + str(id), 'sell').decode('utf-8')
            dec_dict['slot'] = self._r.hget('decoration:' + str(id), 'slot').decode('utf-8')
            dec_dict['craft_price'] = self._r.hget('decoration:' + str(id), 'craft_price').decode('utf-8')
            dec_dict['skills'] = []
            dec_dict['recipes'] = []
            skills = self._r.smembers('decoration:' + str(id) + ':skills')
            for sid in skills:
                temp_skill = {}
                temp_skill['id'] = self._r.hget(sid, 'id').decode('utf-8')
                temp_skill['name'] = self._r.hget(sid, 'name').decode('utf-8')
                temp_skill['value'] = self._r.hget(sid, 'value').decode('utf-8')
                dec_dict['skills'].append(temp_skill)
            recipes = self._r.smembers('decoration:' + str(id) + ':recipes')
            for recipe in recipes:
                temp_recipe = []
                items = self._r.smembers(recipe)
                for item in items:
                    temp_item = {}
                    temp_item['id'] = self._r.hget(item, 'id').decode('utf-8')
                    temp_item['name'] = self._r.hget(item, 'name').decode('utf-8')
                    temp_item['quantity'] = self._r.hget(item, 'quantity').decode('utf-8')
                    temp_recipe.append(temp_item)
                dec_dict['recipes'].append(temp_recipe)
            return dec_dict
        else:
            print('No decoration matching id: %s' % str(id))
            return {}    
    