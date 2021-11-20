import time
import random
import json
from service.systemController import SystemController
from store.mongoStore import MongoStore

def main():
    start = time.time() - 10
    n = 30
    minT = 5
    maxT = 10
    controller = SystemController.getInstance()
    store = MongoStore.getInstance()
    t = 1
    for i in range(n):
        time.sleep(1)
        if not controller.getIsReady():
            time.sleep(1)
        print('opening valve for', t, 'seconds')
        controller.openValve()
        time.sleep(t)
        controller.closeValve()
    end = time.time() + 10
    time.sleep(10)

    with open('data.json', 'w') as f:
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