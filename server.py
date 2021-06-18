import socket

import threading
from time import sleep
import os

import targetcircle
import config
import cv2
import numpy as np

import sys
sys.path.insert(0, './config/')
import configuration as conf


targetPoints = []

def target_founder():
    global targetPoints
    cap = config.open_camera()
    
    bounds = conf.configGetTargetHCVBounds()
    if not bounds:
        print("HCV bouds not found")
        return
    lower,upper = bounds
    
    persp, size, exist = config.get_perspective()
    if not exist:
        print("There is no perspective, reset markers")
        return
    
    ret, frame = cap.read()
    frames_no_found = 0
    last_points = []
    while ret:
        imgOutput = cv2.warpPerspective(frame, persp, size)
        targetPoints = targetcircle.get_target_points(imgOutput,lower,upper)
        if targetPoints:
            last_points = targetPoints
            frames_no_found = 0
        else:
            frames_no_found +=1
            if frames_no_found > 10:
                last_points = []
                targetPoints = []
            else:
                targetPoints = last_points
        ret, frame = cap.read()

    cap.release()

def compare(a, b, encoding="utf8"):
    if isinstance(a, bytes):
        a = a.decode(encoding)
    if isinstance(b, bytes):
        b = b.decode(encoding)
    return a == b

def main():
    mydata = threading.local()
    thread = threading.Thread(target=target_founder)
    thread.start()


    localPort   = 20001
    bufferSize  = 1024
    UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
    UDPServerSocket.bind(('', localPort))
    print("UDP server up and listening")

    width = int(conf.configGetValue("frame_width"))
    height = int(conf.configGetValue("frame_height"))

    while(True):

        bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)
        message = bytesAddressPair[0]
        address = bytesAddressPair[1]
        clientMsg = "Message from Client:{}".format(message)
        clientIP  = "Client IP Address:{}".format(address)
        print(clientMsg)
        print(clientIP)
        
        msgFromServer = "No such command"
        if message == b'gt':#get target points
            msgFromServer       = str(targetPoints)
        if message == b'gs': #get warped window size
            msgFromServer = str((width,height))
        bytesToSend         = str.encode(msgFromServer)

        UDPServerSocket.sendto(bytesToSend, address)





if __name__ == "__main__":
    main()
