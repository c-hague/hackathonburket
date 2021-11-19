import config
import pymongo
from store.store import DataStore
class MongoFactory(object):
    __instance: pymongo.MongoClient = None

    @staticmethod
    def getConnection():
        if MongoFactory.__instance:
            return MongoFactory.__instance
        MongoFactory.__instance = pymongo.MongoClient(config.MONGO_STRING)
        return MongoFactory.__instance

class MongoStore(DataStore):
    __instance = None
    @staticmethod
    def getInstance():
        if MongoStore.__instance:
            return MongoStore.__instance
        return MongoStore()

    def __init__(self):
        client = MongoFactory.getConnection()
        self.db = client[config.DB_NAME]

    def addMass(self, mass):
        self.db[config.MASS_COL].insert_one(mass)
    
    def addState(self, state):
        self.db[config.STATE_COL].insert_one(state)
    
    def addVolume(self, volume):
        self.db[config.VOLUME_COL].insert_one(volume)
    
    def addTime(self, time):
        self.db[config.TIME_COL].insert_one(time)
    
    def getMass(self, startTime, endTime, skip, limit):
        query = {}
        if startTime:
            query['time'] = {'$gte', startTime}
        if endTime:
            if not query['time']:
                query['time'] = {}
            query['time'].update({'$lte', endTime})
        return list(self.db[config.MASS_COL].find(query).limit(limit).skip(skip))

    def getVolume(self, startTime, endTime, skip, limit):
        query = {}
        if startTime:
            query['time'] = {'$gte', startTime}
        if endTime:
            if not query['time']:
                query['time'] = {}
            query['time'].update({'$lte', endTime})
        return list(self.db[config.VOLUME_COL].find(query).limit(limit).skip(skip))

    def getMass(self, startTime, endTime, skip, limit):
        query = {}
        if startTime:
            query['time'] = {'$gte', startTime}
        if endTime:
            if not query['time']:
                query['time'] = {}
            query['time'].update({'$lte', endTime})
        return list(self.db[config.STATE_COL].find(query).limit(limit).skip(skip))

    def getMass(self, startTime, endTime, skip, limit):
        query = {}
        if startTime:
            query['time'] = {'$gte', startTime}
        if endTime:
            if not query['time']:
                query['time'] = {}
            query['time'].update({'$lte', endTime})
        return list(self.db[config.TIME_COL].find(query).limit(limit).skip(skip))