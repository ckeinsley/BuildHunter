import redis

r = redis.StrictRedis(host='433-05.csse.rose-hulman.edu', port=6379, db=0, password='huntallthemonsters247')

#Generate new itemID and add to items set
lastUID = 0
def getUID():
    global lastUID
    r.sadd('items', lastUID)
    lastUID = lastUID + 1
    return lastUID

def createCraftableItem():
    uid = getUID()
    for _ in range(0,3):
        r.sadd(str(uid) + ':components', getUID())
    return uid

testUsers = ['rahul', 'colin', 'chris', 'jack']
buildParts = ['head', 'chest', 'arms', 'waist', 'legs']

for user in testUsers:
    #Add users to user set
    r.sadd('users', user)
    for i in range(0,3):
        #Add builds to user set
        buildID = user + ':builds:' + str(i)
        r.sadd(user + ':builds', buildID)
        #Add parts to each build
        for part in buildParts:
            r.hset(buildID, part, createCraftableItem())
            #Add decoration list to build
            decID = buildID + ':decs'
            for _ in range(0,3):
                r.sadd(decID+':'+part, createCraftableItem())





