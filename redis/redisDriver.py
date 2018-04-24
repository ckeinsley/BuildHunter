import redis

class RedisDriver:

    _r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')

    def __init__(self):
        self._active_user = None
        self._active_build = None

    ####----active_user and active_build properties----####

    @property
    def active_user(self):
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

    @property
    def active_build(self):
        return self._active_build
    
    @active_build.setter
    def active_build(self, build):
        temp = self._active_build
        self._active_build = build
        if self._r.sismember(self.active_user + ":builds", self.get_build_id()):
            self._active_build = temp
            raise ValueError('Build does not exist for the current active user')
            
    @active_build.deleter
    def active_build(self):
        self._active_build = None
    
    def get_build_id(self):
        if self.active_user is None:
            raise ValueError('No active user set.')
        if self.active_build is None:
            raise ValueError('No active build set.')
        return self.active_user + ':build:' + self.active_build

    ####----Users----####
    
    def add_user(self, user, setActive=False):
        #TODO: Input verification
        self._r.sadd('users', user)
        if setActive:
            self.active_user = user

    def delete_user(self, user):
        #TODO
        pass

    ####----Builds----####
    
    def add_build(self, build, setActive=False):
        #TODO
        pass
    
    def delete_build(self, build):
        #TODO
        pass

    def get_all_builds(self):
        #TODO
        pass
    
    def get_build_details(self):
        #TODO
        pass

    ####----Build Components (e.g. armor pieces, weapons)----####

    BUILD_PARTS = ['head', 'chest', 'arms', 'waist', 'legs', 'weapon']

    def add_build_component(self, part, itemId):
        #TODO
        pass

    def remove_build_component(self, part):
        #TODO
        pass
    
    ####----Decorations----####

    def add_decoration(self, part, itemId):
        #TODO
        pass
    
    def remove_decoration(self, part, itemId):
        #TODO
        pass

    def remove_all_decorations(self, part):
        #TODO
        pass

    ####----Items----####

    ITEM_TYPES = ['armor', 'weapon', 'skill', 'item']

    def get_object_name(self, id, type_):
        #TODO: Input verification
        return self._r.hget(type_+ '_ids', id).decode('utf-8')
    
    def get_object_type(self, id):
        #TODO
        pass
    
    def get_object_id(self, name, type_):
        #TODO
        pass
    




