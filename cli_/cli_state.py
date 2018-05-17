import sys

sys.path.insert(0,'../redis_')
sys.path.insert(0,'../kafka_')
sys.path.insert(0,'../cassandra_')
sys.path.insert(0,'../neo4j_')

from redis_ import redisDriver
from kafka_ import producer as prod
from cassandra_ import cassandraDriver as cd
from neo4j_ import neo4jDriver as neoDriver

EMPTY_BUILD = {
            'head' : None,
            'chest' : None,
            'arms' : None,
            'waist' : None,
            'legs' : None,
            'weapon' : None,
            'head:decorations' : [],
            'chest:decorations' : [],
            'arms:decorations' : [],
            'waist:decorations' : [],
            'legs:decorations' : [],
            'weapon:decorations' : []
        }

class CliState:

    def __init__(self):
        self._db = redisDriver.RedisDriver(is_master=False)
        self._active_user = None
        self._active_build = None
        self._local_build = EMPTY_BUILD

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
        else:
            new_parts = self._db.get_build_parts(self.get_build_id())
            self._local_build = EMPTY_BUILD
            for item in new_parts.items():
                self._local_build[item[0].decode('utf-8')] = item[1].decode('utf-8')
                new_decorations = self._db.get_decorations(self.get_build_id(), item[0].decode('utf-8'))
                if new_decorations == None:
                    new_decorations = []
                self._local_build[item[0].decode('utf-8') + ':decorations'] = list(map(lambda x: x.decode('utf-8'), new_decorations))

    @active_build.deleter
    def active_build(self):
        self._active_build = None
        self._local_build = EMPTY_BUILD

    def get_build_id(self):
        return self.active_user + ':' + self.active_build

    ####----Users----####
    
    def add_user(self, user, setActive=False):
        if self._db.is_user(user):
            raise ValueError('User ' + user +  ' already exists')
        else:
            prod.add_user(user)
            #self._db.add_user(user)
            if setActive:
                self.active_user = user

    def delete_user(self, user):
        prod.delete_user(user)
        try:
            if (user is self.active_user):
                del self.active_user
        except:
            pass
        #self._db.delete_user(user)

    def is_user(self, user):
        return self._db.is_user(user)

    ####----Builds----####
    
    def add_build(self, build):
        build_id = self.active_user + ':' + build
        #Add build to user builds
        prod.add_build(self.active_user, build_id)
        #self._db.add_build(self.active_user, build_id)
    
    def delete_build(self, build):
        build_id = self.active_user + ':' + build
        prod.delete_build(self.active_user, build_id, list(self.BUILD_PARTS))
        try:
            if build == self.active_build and self.active_build != None:
                del self.active_build
        except ValueError:
            pass
        #Remove build
        #self._db.delete_build(self.active_user, build_id, self.BUILD_PARTS)

    def get_all_builds(self):
        return self._db.get_all_builds(self.active_user)

    def get_build_by_attr_value(self, attr):
        return neoDriver.generate_build_one(attr)

    ####----Build Components (e.g. armor pieces, weapons)----####

    BUILD_PARTS = {'head', 'chest', 'arms', 'waist', 'legs', 'weapon'}

    # TODO worry about blademaster/gunner/all later
    def add_build_component(self, part, item_id):
        prod.add_build_component(self.get_build_id(), part, item_id)
        self._local_build[part] = item_id
        self._local_build[part+':decorations'] = []
        # self._db.add_build_component(self.get_build_id(), part, item_id)

    def remove_build_component(self, part):
        prod.remove_build_component(self.get_build_id(), part)
        self._local_build[part] = None
        self._local_build[part+':decorations'] = []
        #self._db.remove_build_component(self.get_build_id(), part)
    
    # TODO shouldn't be the get build details method
    def get_build_parts(self):
        #return self._db.get_build_parts(self.get_build_id())
        return {
            'head' : self._local_build.get('head'),
            'chest' : self._local_build.get('chest'),
            'arms' : self._local_build.get('arms'),
            'waist' : self._local_build.get('waist'),
            'legs' : self._local_build.get('legs'),
            'weapon' : self._local_build.get('weapon')
        }
    
    def get_build_resistances(self):
        return cd.getBuildResistances(self.get_build_parts)

    def get_build_skills(self):
        return cd.getBuildSkills(self.get_build_parts)

    def is_part(self, id, part):
        return self._db.is_part(id, part)

    ####----Decorations----####

    # TODO worry about slots taken up by a decoration later
    def add_decoration(self, part, itemId):
        prod.add_decoration(self.get_build_id(), part, itemId)
        self._local_build[part + ':decorations'].append(str(itemId))
        #self._db.add_decoration(self.get_build_id, part, itemId)
    
    def remove_decoration(self, part, itemId):
        prod.remove_decoration(self.get_build_id(), part, itemId)
        self._local_build[part + ':decorations'].remove(str(itemId))
        #self._db.remove_decoration(self.get_build_id, part, itemId)

    def get_decorations(self, part):
        return self._local_build.get(part + ':decorations')
        #return self._db.get_decorations(self.get_build_id(), part)

    def remove_all_decorations(self, part):
        prod.remove_all_decorations(self.get_build_id(), part)
        self._local_build[part + ':decorations'] = []
        #self._db.remove_all_decorations(self.get_build_id, part)

    def is_decoration(self, id):
        return self._db.is_decoration(id)

    def get_decoration_data(self, id):
        return self._db.get_decoration_data(id)

    ####----Items----####

    ITEM_TYPES = {'armor', 'weapon', 'skill', 'item', 'decoration'}

    def get_object_name(self, id, type_):
        result = self._db.get_object_name(id, type_)
        if result is None:
            raise ValueError(str(id) + ' is not a valid ' + type_ + ' ID.')
        return result
    
    def search_object_name(self, name, type_):
        return self._db.search_object_name(name, type_)
        
    def get_object_type(self, id):
        return self._db.get_object_type(id)
    
    def get_object_id(self, name, type_):
        result = self._db.get_object_id(name, type_)
        if result is None:
            raise ValueError(name + ' is not a valid ' + type_ + ' name.')
        return result
    
    def is_object(self, id, type_):
        return self._db.is_object(id, type_)

    def get_item_data(self, id):
        return self._db.get_item_data(id)
        