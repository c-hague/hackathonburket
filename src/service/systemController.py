from random import random
import config
from service.mqttConnection import MQTTConnection
from store.mongoStore import MongoStore
import time
import numpy as np
from service.SysCalibration import Calibrate_System

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
        self.calibrate = Calibrate_System()
    
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
        if len(lastTank) <= 9:
            return None
        masses = np.array(list(map(lambda x: x['mass'], lastTank)))
        slopes: np.ndarray = masses[:-1] - masses[1:]
        return lastTank[0]['mass'] < 20 or (slopes.mean() >= 0).all()

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
    
    def calibrateSystem(self):
        times = []
        for i in range(5):
            self.closeValve()
            self.resetVolume()
            time.sleep(1)
            self._waitRefilling()
            waitTime = 30
            start = time.time()
            self.openValve()
            time.sleep(waitTime)
            self.closeValve()
            self._waitRefilling()
            end = time.time() + 2
            time.sleep(2)
            times.append([start, end])
        self.calibrate.compile_data(times)
        return self.calibrate.calibrate_constants()
        


    def _waitRefilling(self):
        closed = False
        i = 0
        if self.getIsFull():
            self.closeValve()
            closed = True
            while not self.getIsTankMin():
                time.sleep(1)
                i += 1
            self.closeValve()
        if closed:
            self.openValve()
        return closed
    
    def dose(self, amount):
        if amount < 0:
            return 0
        t = self.calibrate.predict(amount)
        self.resetVolume()
        time.sleep(1)
        self._waitRefilling()
        m0 = self.store.getLastFromCollection(config.MASS_COL)
        self.openValve()
        time.sleep(t)
        self.closeValve()
        self._waitRefilling()
        time.sleep(8)
        m1 = self.store.getLastFromCollection(config.MASS_COL)
        return m1[0]['mass'] - m0[0]['mass']

