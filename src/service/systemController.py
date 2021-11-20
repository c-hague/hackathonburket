import config
from service.mqttConnection import MQTTConnection
from store.mongoStore import MongoStore
import time
import numpy as np

class ValveOpenException(Exception):
    pass

class ValveCloseException(Exception):
    pass

class VolumeResetException(Exception):
    pass

class SystemController(object):
    __instance = None
    @staticmethod
    def getInstance():
        if SystemController.__instance:
            return SystemController.__instance
        SystemController.__instance = SystemController()
        return SystemController.__instance

    def __init__(self):
        self.client = MQTTConnection.getInstance()
        self.lastValveState = False
        self.client.loop_start()
        self.store = MongoStore.getInstance()
    
    def getIsReady(self):
        lastState = self.store.getLastNonMaxFillState()
        if len(lastState) <= 0:
            return False
        return lastState[0]['state'] == 'Ready'            

    def getIsFull(self):
        lastState = self.store.getLastFromCollection(config.STATE_COL)
        if len(lastState) <= 0:
            return False
        lastTank = self.store.getLastFromCollection(config.MASS_COL, limit=2)
        if len(lastTank) <= 1:
            return None
        return lastState[0]['state'] == 'Max reached' or lastState[0]['state'] == 'Refilling' or lastTank[0]['mass'] - lastTank[1]['mass'] < 0 or lastTank[0]['mass'] > 5000
    
    def getIsTankMin(self):
        lastTank = self.store.getLastFromCollection(config.MASS_COL, limit=10)
        if len(lastTank) <= 10:
            return None
        masses = np.array(map(lambda x: x['mass']), lastTank)
        slopes: np.ndarray = masses[:-1] - masses[1:]
        return lastTank[0]['mass'] < 20 or slopes.mean() >= 0

    def openValve(self):
        result = self.client.publish(config.PUB_VALVE, 'Open')
        if result[0] != 0:
            raise ValveOpenException(f'Valve Open Error {result[0]}')
        self.store.addCommand({
            'topic': config.PUB_VALVE,
            'command': 'Open',
            'time': time.time()
        })
        self.lastValveState = True
    
    def closeValve(self):
        result = self.client.publish(config.PUB_VALVE, 'Close')
        if result[0] != 0:
            raise ValveCloseException(f'Valve Close Error {result[0]}')
        self.store.addCommand({
            'topic': config.PUB_VALVE,
            'command': 'Close',
            'time': time.time()
        })
        self.lastValveState = False
    
    def resetVolume(self):
        result = self.client.publish(config.PUB_RESET, '1')
        if result[0] != 0:
            raise VolumeResetException(f'Volume Reset Error {result[0]}')
        self.store.addCommand({
            'topic': config.PUB_RESET,
            'command': '1',
            'time': time.time()
        })
