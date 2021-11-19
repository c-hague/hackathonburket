import config
import time

from paho.mqtt import client as mqtt_client

from store.mongoStore import MongoStore
def getClient() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(config.CLIENT_ID)
    client.on_connect = on_connect
    client.connect(config.BROKER, config.PORT)
    return client


    

def main():
    client = getClient()
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
            store.addState({
                'state': msg.payload.decode(),
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
    client.subscribe('#')
    client.on_message = onMessgae
    client.loop_forever()

if __name__ == '__main__':
    main()