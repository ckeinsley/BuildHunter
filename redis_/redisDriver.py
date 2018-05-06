import redis

class RedisDriver:

    _r = None
    #_r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')
    #_r = redis.StrictRedis()

    def __init__(self):
        self._active_user = None
        self._active_build = None

    def connect(self):
        self._r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')

    def check_alive(self):
        try:
            response = self._r.ping()
            return response
        except Exception as ex:
            print(str(ex))
            return False

    ####----active_user and active_build properties----####

    @property
    def active_user(self):
        if self._active_user is None:
            raise ValueError('No active user set.')
        return self._active_user

    @active_user.setter
    def active_user(self, user):
        if self._r.sismember('users', user):
            self._active_user = user
        else:
            raise ValueError(user + ' is not a registered user.')

    @active_user.deleter
    def active_user(self):
        self._active_user = None
        self._active_build = None

    @property
    def active_build(self):
        if self._active_build is None:
            raise ValueError('No active build set.')
        return self._active_build
    
    @active_build.setter
    def active_build(self, build):
        temp = self._active_build
        self._active_build = build
        if not self._r.sismember(self.active_user + ':builds', self.get_build_id()):
            self._active_build = temp
            raise ValueError('Build does not exist for the current active user')
            
    @active_build.deleter
    def active_build(self):
        self._active_build = None
    
    def get_build_id(self):
        return self.active_user + ':' + self.active_build

    ####----Users----####
    
    def add_user(self, user, setActive=False):
        if (self._r.sismember('users', user)):
            raise ValueError('User ' + user +  ' already exists')
        else:
            self._r.sadd('users', user)
            if setActive:
                self.active_user = user

    def delete_user(self, user):
        if (user is self.active_user):
            del self.active_user
        self._r.delete(*self._r.keys(user + ':*'))
        self._r.srem('users', user)

    def is_user(self, user):
        return self._r.sismember('users', user)

    ####----Builds----####
    
    def add_build(self, build):
        buildId = self.active_user + ':' + build

        #Add build to user builds
        self._r.sadd(self.active_user + ":builds", buildId)
    
    def delete_build(self, build):
        buildId = self.active_user + ':' + build
        if build == self.active_build:
            del self.active_build
        #Remove from user build list
        self._r.srem(self.active_user + ":builds", buildId)

        #Delete build hash
        self._r.delete(buildId)

        #Delete decoration sets
        for part in self.BUILD_PARTS:
            self._r.delete(buildId + ':' + part)

    def get_all_builds(self):
        return self._r.smembers(self.active_user + ':builds')
    
    ####----Build Components (e.g. armor pieces, weapons)----####

    BUILD_PARTS = {'head', 'chest', 'arms', 'waist', 'legs', 'weapon'}

    def add_build_component(self, part, itemId):
        self._r.hset(self.get_build_id(), part, itemId)

    def remove_build_component(self, part):
        self._r.hdel(self.get_build_id(), part)
        self._r.delete(self.get_build_id() + ':' + part)
    
    def get_build_parts(self):
        return self._r.hgetall(self.get_build_id())

    def is_part(self, id, part):
        if (part == 'weapon'):
            return self.is_object(id, 'weapon')
        return self._r.sismember('armor:' + part, id)
    
    ####----Decorations----####

    def add_decoration(self, part, itemId):
        self._r.sadd(self.get_build_id + ':' + part, itemId)
    
    def remove_decoration(self, part, itemId):
        self._r.srem(self.get_build_id + ':' + part, itemId)

    def get_decorations(self, part):
        self._r.smembers(self.get_build_id + ':' + part)

    def remove_all_decorations(self, part):
        self._r.delete(self.get_build_id + ':' + part)

    def is_decoration(self, id):
        return self._r.sismember('decoration_ids', id)

    ####----Items----####

    ITEM_TYPES = {'armor', 'weapon', 'skill', 'item', 'decoration'}

    def get_object_name(self, id, type_):
        result = self._r.hget(type_+ '_ids', id)
        if result is None:
            raise ValueError(id + ' is not a valid ' + type_ + ' ID.')
        return result
    
    def search_object_name(self, name, type_):
        return self._r.hscan_iter(type_ + '_names', '*' + name + '*')
        
    def get_object_type(self, id):
        for type_ in self.ITEM_TYPES:
            if self._r.hexists(type_ + '_ids', id):
                return type_
        return None
    
    def get_object_id(self, name, type_):
        result = self._r.hget(type_+ '_names', name)
        if result is None:
            raise ValueError(name + ' is not a valid ' + type_ + ' name.')
        return result
    
    def is_object(self, id, type_):
        return self._r.hget(type_+ '_ids', id) is not None

    
    




