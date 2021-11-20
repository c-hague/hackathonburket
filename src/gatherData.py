import time
import random
import json
import config
import math
import numpy as np
from service.systemController import SystemController
from store.mongoStore import MongoStore
import matplotlib.pyplot as plt
import pandas as pd

def main():
    controller = SystemController.getInstance()
    store = MongoStore.getInstance()
    n = 50
    learningRate = .0001
    b = 190
    target = 500
    errors = []
    bs = []
    try:
        for i in range(n):
            e, _ = trial(controller, store, b, target)
            m = e * math.exp(-i) * learningRate
            b += m if abs(m) < b / 2 else b / 2 * m / abs(m)
            print(b)
            errors.append(e)
            bs.append(b)
    except Exception as e:
        controller.closeValve()
    plt.plot(range(len(errors)), errors)
    plt.savefig('tmp/error.png')
    plt.clf()
    plt.scatter(bs, errors)
    plt.savefig('tmp/b.png')

def getSecondsFromTarget(target):
    b = 190.5
    return target / b



def trial(controller,store, b, target):
    waitAfter = 2
    controller.closeValve()
    controller.resetVolume()
    time.sleep(1)
    waitRefilling(controller)
    waitTime = target / b
    start = time.time()
    controller.openValve()
    time.sleep(waitTime)
    controller.closeValve()
    if waitRefilling(controller):
        return 0, 0
    end = time.time() + waitAfter
    time.sleep(waitAfter)
    
    volumes = pd.DataFrame(store.getVolume(start, end, 0, 2048))
    masses = pd.DataFrame(store.getMass(start, end, 0, 2048))
    plt.plot(volumes['time']-volumes['time'].min(), volumes['volume'])
    plt.plot(masses['time'] - volumes['time'].min(), masses['mass'] - masses['mass'].min())
    plt.plot([0, end - start], [target, target])
    plt.legend(['volume', 'mass', 'target'])
    plt.savefig('tmp/experiment.png')
    mError = (masses['mass'][masses.shape[0] - 1] - masses['mass'].min()) - target
    vError = volumes['volume'][volumes.shape[0] - 1] - target
    print('mass error', mError)
    print('volume error', vError)
    return mError, vError


def waitRefilling(controller: SystemController):
    closed = False
    i = 0
    if controller.getIsFull():
        controller.closeValve()
        closed = True
        print('refilling!')
        while not controller.getIsTankMin():
            time.sleep(1)
            i += 1
        controller.closeValve()
        print('refilling took', i, 'seconds')
    if closed:
        controller.openValve()
    return closed
    
if __name__ == '__main__':
    main()