class DataStore(object):
    def __init__(self):
        pass

    def addState(self, state):
        pass
    
    def addVolume(self, volume):
        pass

    def addMass(self, mass):
        pass
    
    def addTime(self, time):
        pass

    def addFloFlow(self, flow):
        pass

    def addVelocity(self, velocity):
        pass

    def addWeight(self, weight):
        pass

    def addFlow(self, flow):
        pass

    def addTotal(Self, total):
        pass

    def getMass(self, startTime, endTime, skip, limit):
        return []
    
    def getVolume(self, startTime, endTime, skip, limit):
        return []

    def getState(self, startTime, endTime, skip, limit):
        return []

    def getTime(self, startTime, endTime, skip, limit):
        return []

class InMemoryStore(DataStore):
    def __init__(self):
        self.states = []
        self.volumes = []
        self.masses = []
        self.times = []
    
    def addState(self, state):
        self.states.append(state)
    
    def addVolume(self, volume):
        self.volumes.append(volume)
    
    def addMass(self, mass):
        self.masses.append(mass)
    
    def addTime(self, time):
        self.times.append(time)
