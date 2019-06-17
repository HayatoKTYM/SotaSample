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
      builder.characters('layerName', "A")
      builder.characters('actionName', actionName)
      builder.sendMessage()
      continue
    else:
        #builder.characters('actionName', command.decode("shift_jis").encode("euc-jp"))
      
      if "speak" in command:
        content=raw_input('content>')
        builder.characters('content', content.decode("shift_jis").encode("euc-jp"))
      
    builder.characters('layerName', 'A')
    #builder.integer32('autoend', 0)
    #builder.integer32('keep', 1)
    builder.sendMessage()


if __name__ == '__main__':
  main()
    

