import redis

class RedisDriver:

    _r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')
    #_r = redis.StrictRedis()

    def __init__(self):
        pass

    def ping(self):
        try:
            response = self._r.ping()
            return response
        except Exception as ex:
            print(str(ex))
            return False

    ####----active_user and active_build properties----####

    def is_user(self, user):
        return self._r.sismember('users', user)
    
    def build_exists_for_user(self, user, build_id):
        return self._r.sismember(user + ':builds', build_id)

    ####----Users----####

    def add_user(self, user):
        self._r.sadd('users', user)

    def delete_user(self, user):
        self._r.delete(*self._r.keys(user + ':*'))
        self._r.srem('users', user)

    ####----Builds----####
    
    def add_build(self, user, buildId):
        #Add build to user builds
        self._r.sadd(user + ":builds", buildId)
    
    def delete_build(self, user, buildId, build_parts):
        #Remove from user build list
        self._r.srem(user + ":builds", buildId)

        #Delete build hash
        self._r.delete(buildId)

        #Delete decoration sets
        for part in build_parts:
            self._r.delete(buildId + ':' + part)
    
    def get_all_builds(self, user):
        return self._r.smembers(user)
    
    ####----Build Components (e.g. armor pieces, weapons)----####

    BUILD_PARTS = {'head', 'chest', 'arms', 'waist', 'legs', 'weapon'}

    def add_build_component(self, build_id, part, item_id):
        self._r.hset(build_id, part, item_id)

    def remove_build_component(self, part, build_id):
        self._r.hdel(build_id, part)
        self._r.delete(build_id + ':' + part)
    
    def get_build_parts(self, build_id):
        return self._r.hgetall(build_id)

    def is_part(self, id, part):
        if (part == 'weapon'):
            return self.is_object(id, 'weapon')
        return self._r.sismember('armor:' + part, id)
    
    ####----Decorations----####

    def add_decoration(self, build_id, part, itemId):
        self._r.sadd(build_id + ':' + part, itemId)
    
    def remove_decoration(self, build_id, part, itemId):
        self._r.srem(build_id + ':' + part, itemId)

    def get_decorations(self, build_id, part):
        self._r.smembers(build_id + ':' + part)

    def remove_all_decorations(self, build_id, part):
        self._r.delete(build_id + ':' + part)

    def is_decoration(self, id):
        return self._r.sismember('decoration_ids', id)

    ####----Items----####

    ITEM_TYPES = {'armor', 'weapon', 'skill', 'item', 'decoration'}

    def get_object_name(self, id, type_):
        return self._r.hget(type_+ '_ids', id)
    
    def search_object_name(self, name, type_):
        return self._r.hscan_iter(type_ + '_names', '*' + name + '*')
        
    def get_object_type(self, id):
        for type_ in self.ITEM_TYPES:
            if self._r.hexists(type_ + '_ids', id):
                return type_
        return None
    
    def get_object_id(self, name, type_):
        return self._r.hget(type_+ '_names', name)
    
    def is_object(self, id, type_):
        return self._r.hget(type_+ '_ids', id) is not None

    ####----Armor----####

    # TODO May need to import crafting recipes and stuff as weill into this, we'll see
    def add_armor_data(self, armor):
        if self.is_object(int(armor.get('id')), 'armor'):
            self._r.hset('armor:' + str(armor.get('id')), 'part', armor.get('Part'))
            self._r.hset('armor:' + str(armor.get('id')), 'type', armor.get('Type'))
            self._r.hset('armor:' + str(armor.get('id')), 'slot', armor.get('Slot'))

    ####----Item----####

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

    def get_item_data(self, id):
        if True: # self.is_object(id, 'item'):
            item_dict = {}
            item_dict['name'] = self._r.hget('item:' + str(id), 'name')
            item_dict['rarity'] = self._r.hget('item:' + str(id), 'rarity')
            item_dict['carry'] = self._r.hget('item:' + str(id), 'carry')
            item_dict['buy'] = self._r.hget('item:' + str(id), 'buy')
            item_dict['sell'] = self._r.hget('item:' + str(id), 'sell')
            item_dict['combo_list'] = []
            item_dict['gather_locations'] = []
            combo_ids = self._r.smembers('item:' + str(id) + ':combo_list')
            for cid in combo_ids:
                temp_combo = {}
                temp_combo['id_1'] = self._r.hget(cid, 'id_1')
                temp_combo['name_1'] = self._r.hget(cid, 'name_1')
                temp_combo['id_2'] = self._r.hget(cid, 'id_2')
                temp_combo['name_2'] = self._r.hget(cid, 'name_2')
                item_dict['combo_list'].append(temp_combo)
            gather_loc_ids = self._r.smembers('item:' + str(id) + ':gather_locations')
            for locs in gather_loc_ids:
                temp_loc = {}
                temp_loc['rank'] = self._r.hget(locs, 'rank')
                temp_loc['map'] = self._r.hget(locs, 'map')
                temp_loc['area'] = self._r.hget(locs, 'area')
                temp_loc['gather_method'] = self._r.hget(locs, 'gather_method')
                temp_loc['quantity'] = self._r.hget(locs, 'quantity')
                temp_loc['drop_rate'] = self._r.hget(locs, 'drop_rate')
                item_dict['gather_locations'].append(temp_loc)
            return item_dict
        else:
            print('No item matching id: %s' % str(id))
            return {}