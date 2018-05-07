import sys

sys.path.insert(0,'../redis_')

from redisDriver import RedisDriver

class CliState:

    def __init__(self):
        self._db = RedisDriver()
        self._active_user = None
        self._active_build = None

    @property
    def active_user(self):
        if self._active_user is None:
            raise ValueError('No active user set.')
        return self._active_user

    @active_user.setter
    def active_user(self, user):
        if self._db.is_user(user):
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
        if not self._db.build_exists_for_user(self.active_user, self.get_build_id()):
            self._active_build = temp
            raise ValueError('Build does not exist for the current active user')

    @active_build.deleter
    def active_build(self):
        self._active_build = None

    def get_build_id(self):
        return self.active_user + ':' + self.active_build

    ####----Users----####
    
    def add_user(self, user, setActive=False):
        if self._db.is_user(user):
            raise ValueError('User ' + user +  ' already exists')
        else:
            self._db.add_user(user)
            if setActive:
                self.active_user = user

    def delete_user(self, user):
        if (user is self.active_user):
            del self.active_user
        self._db.delete_user(user)

    def is_user(self, user):
        return self._db.is_user(user)

    ####----Builds----####
    
    def add_build(self, build):
        build_id = self.active_user + ':' + build
        #Add build to user builds
        self._db.add_build(self.active_user, build_id)
    
    def delete_build(self, build):
        build_id = self.active_user + ':' + build
        if build == self.active_build:
            del self.active_build
        #Remove build
        self._db.delete_build(self.active_user, build_id, self.BUILD_PARTS)

    def get_all_builds(self):
        return self._db.get_all_builds(self.active_user)

    ####----Build Components (e.g. armor pieces, weapons)----####

    # TODO Need build local build state

    BUILD_PARTS = {'head', 'chest', 'arms', 'waist', 'legs', 'weapon'}

    def add_build_component(self, part, item_id):
        self._db.add_build_component(self.get_build_id(), part, item_id)

    def remove_build_component(self, part):
        self._db.remove_build_component(self.get_build_id(), part)
    
    def get_build_parts(self):
        return self._db.get_build_parts(self.get_build_id())

    def is_part(self, id, part):
        return self._db.is_part(id, partt)

    ####----Decorations----####

    def add_decoration(self, part, itemId):
        self._db.add_decoration(self.get_build_id, part, itemId)
    
    def remove_decoration(self, part, itemId):
        self._db.remove_decoration(self.get_build_id, part, itemId)

    def get_decorations(self, part):
        self._db.get_decorations(self.get_build_id, part)

    def remove_all_decorations(self, part):
        self._db.remove_all_decorations(self.get_build_id, part)

    ####----Items----####

    ITEM_TYPES = {'armor', 'weapon', 'skill', 'item', 'decoration'}

    def get_object_name(self, id, type_):
        result = self._db.get_object_name(type_, id)
        if result is None:
            raise ValueError(id + ' is not a valid ' + type_ + ' ID.')
        return result
    
    def search_object_name(self, name, type_):
        return self._db.search_object_name(type_ , name)
        
    def get_object_type(self, id):
        return self._db.get_object_type(id)
    
    def get_object_id(self, name, type_):
        result = self._db.get_object_id(type_, name)
        if result is None:
            raise ValueError(name + ' is not a valid ' + type_ + ' name.')
        return result