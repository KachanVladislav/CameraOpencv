import pickle
import cv2
import numpy as np
from pathlib import Path
import configparser


def nothing(x):
    pass

test_window_name = "HSV set, Esc - abort, Enter - commit"

def createTrackbars(): # for assignment
    cv2.namedWindow(test_window_name)
    cv2.createTrackbar("H MIN", test_window_name, 0, 179, nothing)
    cv2.createTrackbar("S MIN", test_window_name, 0, 255, nothing)
    cv2.createTrackbar("V MIN", test_window_name, 0, 255, nothing)
    cv2.createTrackbar("H MAX", test_window_name, 179, 179, nothing)
    cv2.createTrackbar("S MAX", test_window_name, 255, 255, nothing)
    cv2.createTrackbar("V MAX", test_window_name, 255, 255, nothing)




def getColorRangeTrackbars():
    h_min = cv2.getTrackbarPos("H MIN", test_window_name)
    s_min = cv2.getTrackbarPos("S MIN", test_window_name)
    v_min = cv2.getTrackbarPos("V MIN", test_window_name)
    h_max = cv2.getTrackbarPos("H MAX", test_window_name)
    s_max = cv2.getTrackbarPos("S MAX", test_window_name)
    v_max = cv2.getTrackbarPos("V MAX", test_window_name)
    return np.array([h_min, s_min, v_min]), np.array([h_max, s_max, v_max])


def get_config():
    config = Path("./config/config.conf")
    if not config.is_file():
        print("Config file was not found, creating...")

def found_hcv_bounds():
    createTrackbars()
    cap = cv2.VideoCapture(2)
    if not cap.isOpened():
        print("Can't open camera")
        return -1
    while True:
        retval, frame = cap.read()
        if not retval:
            print("No image from camera")
            return 
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green, upper_green = getColorRangeTrackbars()
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        contrast_image = cv2.bitwise_and(frame, frame, mask=mask)
        cv2.imshow("mask", contrast_image)
        cv2.imshow("frame", frame)
        key = cv2.waitKey(10)
        print(key) 
        if  key == 27:#Esc
            return
        if key == 13:#Enter
            return lower_green, upper_green
        
        

def main():
    pass

if (__name__ == "__main__"):
    if found_hcv_bounds():
        print("value")
    else:
        print("no value")