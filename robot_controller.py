# -*- coding: utf-8 -*-
"""
Robot身体制御
"""
__author__ = "Yuto Akagawa"

import os.path
import sys
import time
import random
from monea_connector import MoneaConnector
from utterance_generator import UtteranceGenerator
from conversation_manager import ConversationManager
from utterance_state import UtteranceState
from NLU import RecognitionResultManager, NLU
from logger import Logger
from csv_processing import CSVProcessing
os.environ["REGISTRY_SERVER_PORT"]="25001"

class RobotController:
    def __init__(self):
        self.connector = MoneaConnector('xml/moduleWoz.xml')
        time.sleep(1)
        self.remote_ad = self.connector.context.getRemoteModule('ActionDecoder')
        self.remote_adt = self.connector.context.getRemoteModule('ActionDecoderTree')
        self.remoteA = self.connector.context.getRemoteModule('SR2')
        self.utter_gen = UtteranceGenerator()
        self.conv_manager = ConversationManager()
        #self.logger = Logger()
        us = UtteranceState(self.remote_adt, self.logger, self.conv_manager)
        self.rrmA = RecognitionResultManager(self.remoteA, self.logger, "A")
        self.nluA = NLU(self.rrmA)
        self.preorder = ""
        self.detail_dict = {}
        self.csv = CSVProcessing()
        self.flag=0

    def control_face(self):
        while 1:
            key = getch.getch()
            if key == "j": #J: Look A
                self.look("A")
            elif key == "k": #K: Nod
                self.nod()
            elif key == "l": #L: Look B
                self.look("B")

    def send_message(self, message):
        builder = self.remote_ad.newProcessingRequestBuilder('play')
        builder.characters('actionName', message.decode('utf-8').encode('euc_jp'))
        builder.sendMessage()

    def look(self, target):
        order = 'ln[t='+ target +']'
        print '命令文:'+ order
        self.logger.stamp('look', 'NONE', target, 'NONE')
        self.send_message(order)
        return self.conv_manager.get_topic_memory_list()


    def utter(self, message, detail):
        target = detail#AorB
        order = 'ln[t='+ target +']'
        self.send_message(order)
        topic_memory = self.conv_manager.get_topic_memory()#ジャンルをkeyとしたトピックリスト
        topic = self.conv_manager.get_topic()#現在のtopicを取得
        detail_list = ["abstract", "review", "evaluation", "actor", "director"]
        isActiveDetail = False
        if "active" in message:
            isActiveDetail = True

        if "response-passive" in message:#コマンドが応答
            self.logger.stamp(message, topic, target, "Recognizing")#コマンド実行タイミングをtimestamp
            order = None
            if target == "A":
                if topic == 'NONE': #まだトピックが１つも出てない
                    order = "recommendation"
                else:
                    order = self.nluA.check_keyword()
            elif target == "B":
                if topic == 'NONE':#まだトピックが１つも出てない
                    order = "recommendation"
                else:
                    order = self.nluB.check_keyword()

            print order
            if order == None:#聞き返し
                order = "pardon"

            elif order == "recommendation":#推薦
                order += "-random"
                if target == "A":
                    genre = self.nluA.select_genre(self.conv_manager)
                    print genre
                elif target == "B":
                    genre = self.nluB.select_genre(self.conv_manager)

                topic, genre = self.utter_gen.random_choice(genre, topic_memory)
                if topic != None:
                    self.change_topic(topic, "R", genre)

            elif order in detail_list:
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            print order

        elif "yes-passive" in message or "no-passive" in message:
            self.logger.stamp(message, topic, target, "Recognizing")
            order = None
            #print target
            """
            if target == "A":
                order = self.nluA.check_keyword()
            elif target == "B":
                order = self.nluB.check_keyword()
            print order
            """
            if order == None:
                if "yes" in message:
                    order = "yes"
                elif "no" in message:
                    order = "no"

        elif "detail-active" in message:
            if len(self.detail_dict[topic]) == 0:
                order = "followup"
            else:
                # 過去に発話していないものからランダムで選択
                src_set = set(detail_list)
                tag_set = set(self.detail_dict[topic])
                matched_list = list(src_set & tag_set)
                order = random.choice(matched_list)
                self.detail_dict[topic].pop(self.detail_dict[topic].index(order))


        elif "repeat" in message:
            order = self.preorder
        else: #誤り訂正発話
            if "recommendation" in message:
                order = "recommendation"
                c=0
                if target == "A":
                    if self.flag==1:
                        genre = self.conv_manager.get_current_genre()
                        c=1
                        self.flag=0

                    else:genre = self.nluA.select_genre(self.conv_manager)

                elif target == "B":
                    if self.flag==1:
                        genre = self.conv_manager.get_current_genre()
                        c=1
                        self.flag=0

                    else:genre = self.nluB.select_genre(self.conv_manager)

                topic, genre = self.utter_gen.random_choice(genre, topic_memory,c)
                if topic != None:
                    self.change_topic(topic, "R", genre)
                print topic

            elif "title" in message:
                order = "title"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "genre" in message:
                order = "genre"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "abstract" in message:
                order = "abstract"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "review" in message:
                order = "review"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "evaluation" in message:
                order = "evaluation"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "actor" in message:
                order = "actor"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "director" in message:
                order = "director"
                if order in self.detail_dict[topic]:
                    self.detail_dict[topic].pop(self.detail_dict[topic].index(order))
            elif "unknown" in message:
                order = "unknown"
            elif "yes" in message:
                order = "yes"
            elif "no" in message:
                order = "no"
            else:
                order = message
        self.preorder = order
        utterance = self.utter_gen.generate(order, topic_memory, topic = topic, isActiveDetail=isActiveDetail)
        if utterance != '':
            order = '{ln_and_speak['+ utterance +']}[t='+ target +',d=300]'
            print '命令文:'+ order
            self.send_message(order)
            self.logger.stamp(message, topic, target, utterance)
        else:
            print "Utterance is none::" + message
            self.send_message(order)
            self.logger.stamp(message, topic, target, utterance)

        return self.conv_manager.get_topic_memory_list()

    def terminate(self, detail):
        self.logger.write(detail)
        self.conv_manager.flash_topic_memory_list()
        self.csv.write(self.topic_file_path, self.conv_manager.get_topic_memory_list())

    def nod(self, target):
        order = 'nod'
        print '命令文:'+ order
        self.logger.stamp('nod', 'NONE', target, 'NONE')
        self.send_message(order)
        return self.conv_manager.get_topic_memory_list()

if __name__ == '__main__':
    bc = RobotController()
    bc.look('A')
    bc.utter('actor', 'none')
