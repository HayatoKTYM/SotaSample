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
      builder.characters('layerName', 'C')
      builder.characters('actionName', actionName)
      builder.sendMessage()
      continue
    elif command == "ppap":
      ppap1="{le[x=-60,d=300]_then_speak[ピーピーエーピー]_then_le[x=10,d=200]}"
      ppap21="{{l_elb_and_r_elb}[x=-35]_and_{l_sho_and_r_sho}[x=10]_and_body_y[x=-20]}_then_{{l_elb_and_r_elb}[x=-35]_and_{l_sho_and_r_sho}[x=-10]}"
      ppap22="{{l_elb_and_r_elb}[x=-35]_and_{l_sho_and_r_sho}[x=0]_and_body_y[x=20]}_then_{{l_elb_and_r_elb}[x=-20]_and_{l_sho_and_r_sho}[x=-10]}"
      ppap2="{"+ppap21+"_then_"+ppap22+"_then_"+ppap21+"_then_"+ppap22+"}[d=220]"
      ppap3="{body_y[x=0]_and_r_sho[x=0]_and_r_elb[x=-40]_and_speak}"
      ppap4="{l_sho[x=0]_and_l_elb[x=-40]_and_speak}"
      ppap5="{l_elb_and_r_elb}[x=-20]_then_{wait[x=500]_then_{l_elb_and_r_elb}[x=-40]}_and_{wait[x=200]_then_speak[おーん]}"
      ppap6="{body_y[x=-120]_then_wait[x=300]_then_speak_then_wait[x=300]_then_{body_y_and_head_y_and_r_elb_and_l_elb}[x=0,d=150]}"
      ppap7="{ln[x=-180,d=3000]}"
      ppap8="{{head_y_and_body_y}[x=0,d=100]_and_speak}"
      ppap9="{{r_elb_and_l_elb}[x=0]_and_{l_sho_and_r_sho}[x=30]}"
      ppap10="{{l_sho_and_r_sho}[x=0]}"
      ppap11="{{l_sho_and_r_sho}[x=0]_and_{r_elb_and_l_elb}[x=-40]_and_head_r[x=15]}"
      time.sleep(1.8)
      ppap=ppap1#+"_then_"+ppap2#+"_then_"+ppap3+"[あいハバぺーン]"+"_then_"+ppap4+"[あいハバあっぽー]"+"_then_"+ppap5+"_then_"+ppap6+"[アポおペーン]"
      builder = remote_sota.newProcessingRequestBuilder('play')
      builder.characters('actionName', ppap.decode("utf-8").encode("euc-jp"))
      builder.characters('layerName', 'C')
      builder.integer32('autoend', 1)
      builder.integer32('keep', 1)
      builder.sendMessage()
      continue


    elif command == "le":
      builder.characters('actionName', 'le')
      builder.characters('target', 'B')
      builder.characters('layerName', 'C')
      builder.integer32('autoend', 0)
      builder.integer32('keep', 1)
      builder.sendMessage()
      continue
    elif command == "home":
      builder.characters('actionName', 'home')
      builder.characters('layerName', 'C')
      builder.integer32('keep', 1)
      builder.sendMessage()
      continue
    else:
      builder.characters('actionName', command.decode("shift_jis").encode("euc-jp"))
      if "speak" in command:
        content=raw_input('content>')
        builder.characters('content', content.decode("shift_jis").encode("euc-jp"))
    builder.characters('layerName', 'C')
    #builder.integer32('autoend', 1)
    builder.integer32('keep', 1)
    builder.sendMessage()

if __name__ == '__main__':
  main()
