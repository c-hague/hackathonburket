from store.mongoStore import MongoStore
import config
import pprint
import json

def writeFile(store, start, end, fname, dataLimit):
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
    

def main():
    store = MongoStore.getInstance()
    lastCommands = list(store.db[config.COMMAND_COL].find().sort('time', -1).limit(100))
    commandPairs = []
    state = 0
    currentPair = []
    for i in range(len(lastCommands)):
        if state == 0:
            if lastCommands[i]['command'] == 'Close':
                currentPair.append(i)
                state = 1
        elif state == 1:
            if lastCommands[i]['command'] == 'Open':
                currentPair.append(i)
                commandPairs.append(currentPair)
                currentPair = []
                state = 0
            elif lastCommands[i]['command'] == 'Close':
                currentPair[0] = i
    pprint.pprint(commandPairs)
    for pair in commandPairs:
        writeFile(store,lastCommands[pair[1]]['time'], lastCommands[pair[0]]['time'], 'tmp/trial_{0}_{1}.json'.format(pair[0], pair[1]), int(1e6))


if __name__ == '__main__':
    main()