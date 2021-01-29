#!usr/bin/env python
# -*- coding: utf-8 -*- 

import json

class MqttSubscribeObject:
    topic = ""
    messageCallBack = None
    def __init__(self, topic, messageCallBack):
        self.topic = topic
        self.messageCallBack = messageCallBack

    def callBack(self, topic, payload, **kwargs):
        # print(topic)
        # print(payload)
        # print(kwargs)
        self.messageCallBack(json.loads(payload))
