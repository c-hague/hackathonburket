from paho.mqtt import client as mqtt_client
import config
import uuid

class MQTTConnection(object):
    __instance: mqtt_client = None
    @staticmethod
    def getInstance() -> mqtt_client:
        if MQTTConnection.__instance:
            return MQTTConnection.__instance
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                print("Connected to MQTT Broker!")
            else:
                print("Failed to connect, return code %d\n", rc)

        client = mqtt_client.Client(config.CLIENT_ID + str(uuid.uuid1()))
        client.on_connect = on_connect
        client.connect(config.BROKER, config.PORT)
        MQTTConnection.__instance = client
        return client