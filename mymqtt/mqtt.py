#!usr/bin/env python
# -*- coding: utf-8 -*- 

# awsのサンプルを使用した形式に書き換え
# iot側の設定や証明書も必要
import signal
import json
import sys

from awscrt import io, mqtt, auth, http
from awsiot import mqtt_connection_builder

from time import sleep
import threading

class MqttObj:
    mqtt_connection = None
    publish_obj = []
    subscribe_obj = []
    publishLoop = None
    exit = False
    def __init__(self):
        pass

    def register_publish(self, mqtt_publish_obj):
        self.publish_obj.append(mqtt_publish_obj)
    def register_subscribe(self, mqtt_subscribe_obj):
        self.subscribe_obj.append(mqtt_subscribe_obj)

    def start(self,endpoint, clientId, certPath, keyPath, rootCaPath):
        event_loop_group = io.EventLoopGroup(1)
        host_resolver = io.DefaultHostResolver(event_loop_group)
        client_bootstrap = io.ClientBootstrap(event_loop_group, host_resolver)
        mqtt_connection = mqtt_connection_builder.mtls_from_path(
                    endpoint=endpoint,
                    cert_filepath=certPath,
                    pri_key_filepath=keyPath,
                    client_bootstrap=client_bootstrap,
                    ca_filepath=rootCaPath,
                    client_id=clientId,
                    clean_session=False,
                    keep_alive_secs=60
                    )

        print("Connecting to {} with client ID '{}'...".format(endpoint, clientId))
        # Make the connect() call
        connect_future = mqtt_connection.connect()
        # Future.result() waits until a result is available
        connect_future.result()
        print("Connected!")

        self.mqtt_connection = mqtt_connection

        # register subscribe
        for subscribeObj in self.subscribe_obj:
            sf, _ = mqtt_connection.subscribe(subscribeObj.topic, mqtt.QoS.AT_LEAST_ONCE, subscribeObj.callBack)
            sf.result()

        # register publish
        publishLoop = threading.Thread(target=self.__publishLoop)
        publishLoop.setDaemon(True)
        publishLoop.start()
        self.publishLoop = publishLoop

    def __publishLoop(self):
        while True:
            for publish_obj_elem in self.publish_obj:
                publish_obj_elem.execute(self.mqtt_connection)
            if self.exit:
                break
            sleep(1)

    def stop(self):
        # stop publish loop
        self.exit = True
        self.publishLoop.join()
        disconnect_future = self.mqtt_connection.disconnect()
        disconnect_future.result()
