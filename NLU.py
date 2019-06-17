# -*- coding: utf-8 -*-

"""
言語理解モジュール
"""
__author__ = "Yuto Akagawa"

import os
import os.path
import sys
import time
from monea_connector import MoneaConnector
import threading
#from logger import Logger
import MySQLdb
os.environ["REGISTRY_SERVER_PORT"]="25001"

class RecognitionResultManager:
    def __init__(self, remote, personID):
        self.remote = remote
        #self.logger = logger
        self.spreco_memory = []
        self.recognizing = ""
        self.personID = personID
        thr=threading.Thread(target=self.watcher)
        thr.setDaemon(True)
        thr.start()

    def watcher(self):
        pretext = ''
        while 1:
            self.remote.timedUpdate(-1)
            #order = self.remote.getAsString("01_RecognizeText").decode("euc-jp")
            spreco = self.remote.getAsString("01_RecognizeText")
            recognizing = self.remote.getAsString("Recognizing")
            audioID = self.remote.getAsString("AudioID")
            self.set_recognizing(recognizing)
            print("recognizing::",recognizing)
            
            if pretext != spreco and spreco != "" and recognizing == "0":
                print spreco
                self.set_spreco(spreco)
                #print self.get_spreco_memory()[-1].decode("utf-8").encode("utf-8")
                #認識結果のログを残す
                #self.logger.stamp("SpReco", "NONE", self.personID, spreco)
                pretext = spreco

    def set_spreco(self, spreco):
        """
        認識結果を保存しておく
        """
        if spreco != "":
            self.spreco_memory.append(spreco)
            if len(self.spreco_memory) > 5:
                self.spreco_memory.pop(0)

    def set_recognizing(self, recognizing):
        if recognizing == "1":
            self.recognizing = True
        else:
            self.recognizing = False

    def get_recognizing(self):
        return self.recognizing

    def get_spreco_memory(self):
        return self.spreco_memory

    def pop_spreco_memory(self, element):
        print "pop"
        index = self.spreco_memory.index(element)
        self.spreco_memory.pop(index)

    """
    reset_spreco_memoryは2018/6/7に追加
    ：Systemが応答するたびにA,Bの発話履歴を消してしまおう
    """
    def reset_spreco_memory(self):
        self.spreco_memory=[]


#6/21

if __name__ == '__main__':
    #l = Logger()
    connector = MoneaConnector('xml/moduleWoz.xml')
    time.sleep(1)
    remoteA = connector.context.getRemoteModule('SR2')
    
    rrm = RecognitionResultManager(remoteA, "A")
    time.sleep(15)

