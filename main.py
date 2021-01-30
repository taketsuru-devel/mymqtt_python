#!usr/bin/env python
# -*- coding: utf-8 -*- 

import sys
import os
import signal

from mqtt import MqttObj
from mqtt_publish_object import MqttPublishObject
from mqtt_subscribe_object import MqttSubscribeObject

if __name__ == "__main__":
    mqtt = None

    def __on_exit(signum, frame):
        print("signal "+str(signum)+" received")
        mqtt.stop()
        print("exit")
        sys.exit(None)

    mqtt = MqttObj()
            
    signal.signal(signal.SIGTERM, __on_exit)
    signal.signal(signal.SIGINT, __on_exit)

    publishObj = MqttPublishObject("test/pub", 5, lambda: {"test": "testvalue"} )
    subscribeObj = MqttSubscribeObject("test/pub", lambda mesDict: print(mesDict.get("test", "ttt")))
    mqtt.register_publish(publishObj)
    mqtt.register_subscribe(subscribeObj)

    mqtt.start(
        endpoint   = os.environ["ENDPOINT"],
        clientId   = os.environ["CLIENT_ID"], 
        certPath   = os.environ["CERT_PATH"],
        keyPath    = os.environ["KEY_PATH"],
        rootCaPath = os.environ["ROOT_CA_PATH"]
    )
    print("start!")
    signal.pause()

