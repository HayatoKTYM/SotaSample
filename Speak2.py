# -*- coding:utf-8 -*-

from monea_connector import MoneaConnector
import math
import threading
import time
import os
os.environ["REGISTRY_SERVER_PORT"] = "25001"


def main():

  connector = MoneaConnector("xml/sample.xml")
  time.sleep(1)
  remote_sota = connector.context.getRemoteModule('decoder')

  while 1:
    command=raw_input('command>')
    builder = remote_sota.newProcessingRequestBuilder('play')
    if command == "cancel":
      actionName=raw_input('actionName>')
      builder = remote_sota.newProcessingRequestBuilder('cancel')
      builder.characters('layerName', 'A')
      builder.characters('actionName', actionName)
      builder.sendMessage()
      continue
    else:
      #builder.characters('actionName', command.decode("shift_jis").encode("euc-jp"))
      builder = remote_sota.newProcessingRequestBuilder('play')####
      builder.characters('actionName', command.decode("utf-8").encode("euc-jp"))
      builder.characters('layerName', 'C')
      builder.integer32('autoend', 1)
      builder.integer32('keep', 1)
      builder.sendMessage()

#{ln_and_speak[宮崎駿だよああああああああああああああああああああああああ]}[t=A]_then_{ln_and_speak[ととろは知ってる]}[t=B]
#"{lt_and_speak[朝ごはんの歌が好きだ]}[t=B]"
if __name__ == '__main__':
  main()
