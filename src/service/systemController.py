import config
from service.mqttConnection import MQTTConnection

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

    def openValve(self):
        if not self.lastValveState:
            result = self.client.publish(config.PUB_VALVE, 'Open')
            if result[0] != 0:
                raise ValveOpenException(f'Valve Open Error {result[0]}')
            self.lastValveState = True
    
    def closeValve(self):
        if self.lastValveState:
            result = self.client.publish(config.PUB_VALVE, 'Close')
            if result[0] != 0:
                raise ValveCloseException(f'Valve Close Error {result[0]}')
            self.lastValveState = False
    
    def resetVolume(self):
        result = self.client.publish(config.PUB_RESET, '1')
        if result[0] != 0:
            raise VolumeResetException(f'Volume Reset Error {result[0]}')
