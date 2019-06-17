# -*- coding:utf-8 -*-

from monea_connector import MoneaConnector
import math
import threading
import time
import os
os.environ["REGISTRY_SERVER_PORT"] = "25001"
connector = MoneaConnector("../xml/sample.xml")
remote_sota = connector.context.getRemoteModule('decoder')
builder = remote_sota.newProcessingRequestBuilder('play')

speak_list = {"a":"こんにちは",
                "b":"ありがとう",
                "c":"ごめんね",
                "d":"さようなら",
                "e":"よろしくお願いします",
                "f":"お名前を教えてください"
                }

def action(command,detail):
    #connector = MoneaConnector("xml/sample.xml")
    #remote_sota = connector.context.getRemoteModule('decoder')
    #builder = remote_sota.newProcessingRequestBuilder('play')
    if command == "look":
        action = "ln[x=%s,d=300]"%detail
    elif command == "head_p":
        action = "head_p[x=%s,d=300]"%detail
    elif command == "incline":
        action = "head_r[x=%s,d=300]"%detail
    elif command == "speak":
        action = "speak[%s]"%speak_list[detail]
    else :
        action = "%s[x=%s,d=300]"%(command,detail)
    builder = remote_sota.newProcessingRequestBuilder('play')
    builder.characters('actionName', action.decode("utf-8").encode("euc-jp"))
    builder.characters('layerName', 'C')
    builder.integer32('autoend', 1)
    builder.integer32('keep', 1)
    builder.sendMessage()
    time.sleep(0.5)
