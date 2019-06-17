# -*- coding: utf-8 -*-
import time
import argparse
import cv2
import os
import numpy as np
import openface
import random
import threading
import concurrent.futures
from monea_connector import MoneaConnector
from NLU import RecognitionResultManager
np.set_printoptions(precision=2)

fileDir = os.path.dirname(os.path.realpath(__file__))
modelDir = os.path.join('/Users/dialog/openface/models')
dlibModelDir = os.path.join(modelDir, 'dlib')
openfaceModelDir = os.path.join(modelDir, 'openface')
with open("stop_monitor.txt","w") as f:
    f.write("start")

def actiongenerator(command="speak[初めまして。あなたのお名前を教えてください。]",flag=False):
    builder = remote_adt.newProcessingRequestBuilder('play')
    builder.characters('actionName', command.decode("utf-8").encode("euc-jp"))
    builder.characters('layerName', 'C')
    builder.integer32('autoend', 1)
    #builder.integer32('keep', 1)
    builder.sendMessage()
    if flag: time.sleep(1)

def cam(video_capture):
    while True:
        ret, frame = video_capture.read()
        if frame is None: continue
        rgbImg = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        bb = align.getAllFaceBoundingBoxes(rgbImg)
        cv2.imshow('dialogue', frame)
        if cv2.waitKey(100) & 0xFF == ord('q'):
            with open("stop_monitor.txt","w") as f:
              f.write("Stop")
              break
        if len(bb) is 0: continue
        with open("stop_monitor.txt","w") as f:
            f.write("Stop")
        break
    
    video_capture.release()
    cv2.destroyAllWindows()

def look():
    
    while 1:
        actiongenerator(command = "{ln[x=30,d=300]}",flag=True)
        time.sleep(5)
        with open("stop_monitor.txt") as g:
            if g.readline() == "Stop": break
        #time.sleep(5)
        actiongenerator(command = "{ln[x=-30,d=300]}",flag=True)
        time.sleep(5)
        with open("stop_monitor.txt") as g:
            if g.readline() == "Stop": break
        #time.sleep(5)


if __name__ == '__main__':
    connector = MoneaConnector("xml/moduleWoz.xml")
    remoteA = connector.context.getRemoteModule('SR2')
    rrm = RecognitionResultManager(remoteA, "A")
    time.sleep(1)
    remote_sota = connector.context.getRemoteModule('decoder')
    remote_adt = connector.context.getRemoteModule('ActionDecoderTree')
    builder = remote_adt.newProcessingRequestBuilder('play')
    builder.characters('actionName', 'home')
    builder.characters('layerName', 'C')
    builder.integer32('keep', 1)
    builder.sendMessage()

    parser = argparse.ArgumentParser()
    parser.add_argument('--dlibFacePredictor',type=str,
        help="Path to dlib's face predictor.",
        default=os.path.join(dlibModelDir,
            "shape_predictor_68_face_landmarks.dat"))
    parser.add_argument('--networkModel',type=str,
        help="Path to Torch network model.",
        default=os.path.join(openfaceModelDir,
            'nn4.small2.v1.t7'))
    parser.add_argument('--width', type=int, default=400)
    parser.add_argument('--height', type=int, default=300)
    parser.add_argument('--fps', type=int, default=5)

    args = parser.parse_args()
    align = openface.AlignDlib(args.dlibFacePredictor)

    video_capture = cv2.VideoCapture(0)
    video_capture.set(3, args.width)
    video_capture.set(4, args.height)
    video_capture.set(5, args.fps)
    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    executor.submit(look)
    executor.submit(cam(video_capture))
    time.sleep(2)
    actiongenerator()
    
    
    while 1:
    
        
        if len(rrm.get_spreco_memory()) == 0: continue
        context = rrm.get_spreco_memory()[-1].decode('utf-8').encode("utf-8")
        if context == "さようなら":
            actiongenerator("speak[おやすみなさい]")
            break
        command = "speak["+context+"]"
        actiongenerator(command)
        rrm.reset_spreco_memory()
        time.sleep(2)






