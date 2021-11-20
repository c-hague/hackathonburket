import config
import time
from store.mongoStore import MongoStore
from service.mqttConnection import MQTTConnection

    

def main():
    client = MQTTConnection.getInstance()
    store = MongoStore.getInstance()
    def onMessgae(client, userdata, msg):
        if msg.topic == config.SUB_MASS:
            try:
                store.addMass({
                    'mass': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_MASS
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_STATE:
            state = msg.payload.decode()
            store.addState({
                'state': state,
                'time': time.time(),
                'topic': config.SUB_STATE
            })
        elif msg.topic == config.SUB_VOLUME:
            try:
                store.addVolume({
                    'volume': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_VOLUME
                })
            except:
                pass
        elif msg.topic == config.SUB_TIME:
            try:
                store.addTime({
                    'data_time': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_TIME
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_FLO_FLOW:
            try:
                store.addFloFlow({
                    'flow': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_FLO_FLOW
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_VELOCITY:
            try:
                store.addVelocity({
                    'velocity': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_VELOCITY
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_WEIGHT:
            try:
                store.addWeight({
                    'weight': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_WEIGHT
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_FLOW:
            try:
                store.addFlow({
                    'flow': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_FLOW
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_TOTAL:
            try:
                store.addTotal({
                    'total': float(msg.payload.decode()),
                    'time': time.time(),
                    'topic': config.SUB_TOTAL
                })
            except ValueError:
                pass
        elif msg.topic == config.SUB_FLO_TIME:
            pass
        else:
            print('message from topic', msg.topic)
    client.subscribe(config.SUB_STATE)
    client.subscribe(config.SUB_MASS)
    client.subscribe(config.SUB_TIME)
    client.subscribe(config.SUB_VOLUME)
    client.subscribe(config.SUB_FLO_FLOW)
    client.subscribe(config.SUB_VELOCITY)
    client.subscribe(config.SUB_WEIGHT)
    client.subscribe(config.SUB_FLOW)
    client.subscribe(config.SUB_TOTAL)
    client.on_message = onMessgae
    client.loop_forever()

if __name__ == '__main__':
    main()