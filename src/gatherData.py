import time
import random
import json
import numpy as np
from service.systemController import SystemController
from store.mongoStore import MongoStore

def main():
    start = time.time() - 10
    n = 10
    minT = 5
    maxT = 10
    reFillTime = 35
    controller = SystemController.getInstance()
    store = MongoStore.getInstance()
    controller.resetVolume()
    t = 30
    for i in range(n):
        if not controller.getIsReady():
            print('paused!')
            time.sleep(1)
        controller.resetVolume()
        waitRefilling(controller, reFillTime)
        print('opening valve for', t, 'seconds')
        controller.openValve()
        for j in np.linspace(0, t, 10):
            waitRefilling(controller, reFillTime)
            time.sleep(t / 10)
        controller.closeValve()
        time.sleep(10)
        end = time.time() 
        writeFile(store, start, end, '30s_{0}.json'.format(i))
    time.sleep(10)

def waitRefilling(controller, dt):
    closed = False
    if controller.getIsFull():
        controller.closeValve()
        closed = True
        print('refilling!')
        time.sleep(dt)
        controller.closeValve()
        dt += dt if dt < 5 else 0
    if closed:
        controller.openValve()

def writeFile(store, start, end, fname, dataLimit=2048):
    dataLimit = 2048
    with open(fname, 'w') as f:
        mass = store.getMass(start, end, 0, dataLimit)
        volume = store.getVolume(start, end, 0, dataLimit)
        dataTime = store.getTime(start, end, 0 ,dataLimit)
        floFlow = store.getFloFlow(start, end, 0, dataLimit)
        velocity = store.getVelocity(start, end, 0, dataLimit)
        weight = store.getWeight(start, end, 0, dataLimit)
        flow = store.getFlow(start, end, 0, dataLimit)
        total = store.getTotal(start, end, 0, dataLimit)
        state = store.getState(start, end, 0, dataLimit)
        l = mass + volume + dataTime + floFlow + velocity + weight + flow + total + state
        json.dump(l, f)
    
if __name__ == '__main__':
    main()