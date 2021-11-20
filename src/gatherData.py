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
    controller = SystemController.getInstance()
    store = MongoStore.getInstance()
    controller.resetVolume()
    t = 30
    for i in range(n):
        if not controller.getIsReady():
            print('paused!')
            time.sleep(1)
        controller.resetVolume()
        waitRefilling(controller, 30)
        print('opening valve for', t, 'seconds')
        controller.openValve()
        for j in np.linspace(0, t, 10):
            waitRefilling(controller, 30)
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

def writeFile(store, start, end, fname):
    with open(fname, 'w') as f:
        mass = store.getMass(start, end, 0, 256)
        volume = store.getVolume(start, end, 0, 256)
        dataTime = store.getTime(start, end, 0 ,256)
        floFlow = store.getFloFlow(start, end, 0, 256)
        velocity = store.getVelocity(start, end, 0, 256)
        weight = store.getWeight(start, end, 0, 256)
        flow = store.getFlow(start, end, 0, 256)
        total = store.getTotal(start, end, 0, 256)
        state = store.getState(start, end, 0, 256)
        l = mass + volume + dataTime + floFlow + velocity + weight + flow + total + state
        json.dump(l, f)
    
if __name__ == '__main__':
    main()