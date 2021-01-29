#!usr/bin/env python
# -*- coding: utf-8 -*- 

# awsのサンプルを使用した形式に書き換え
# iot側の設定や証明書も必要
import signal
import json
import sys
from awscrt import io, mqtt, auth, http

class MqttPublishObject:
    topic = ""
    count = 0
    cycle = 1
    messageGenFunc = None
    def __init__(self, topic, cycle, messageGenFunc):
        self.topic = topic
        self.cycle = cycle
        self.messageGenFunc = messageGenFunc

    def execute(self, mqttObj):
        cnt = self.count+1
        if cnt >= self.cycle:
            mqttObj.publish(topic=self.topic, payload=json.dumps(self.messageGenFunc()), qos=mqtt.QoS.AT_LEAST_ONCE)
            cnt = 0
            # print("published")
        self.count = cnt
