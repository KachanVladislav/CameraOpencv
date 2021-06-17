import argparse
import cv2
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, './config/')
import configuration as conf
import config






def get_target_points(frame, lower_hcv_bound, upper_hcv_bound):
    points = []
    
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv_frame, lower_hcv_bound, upper_hcv_bound)
    contrast_image = cv2.bitwise_and(frame, frame, mask=mask)
    imgBlur = cv2.GaussianBlur(contrast_image,(3, 3),1)
    imgCanny = cv2.Canny(imgBlur,50,50)
    contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    
    for cnt in contours:
        area = cv2.contourArea(cnt)
        # print(area)
        if area>100:#papugai
            cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)
            perimetr =  cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt,0.02*perimetr,True)
            x, y, w, h = cv2.boundingRect(approx)
            points.append([x+w//2, y+h//2])
    cv2.imshow("qwe", frame)
    # cv2.waitKey(10)
    return points


def main():
    cap = config.open_camera()
    # config.show_warped(cap)
    bounds = conf.configGetTargetHCVBounds()
    if not bounds:
        print("HCV bouds not found")
        return False
    lower,upper = bounds

    persp, size, exist = config.get_perspective()
    if not exist:
        print("There is no perspective, reset markers")
        return     
    last_points = []
    points = []
    frames_no_found = 0    
    while True:
        ret, frame = cap.read()
        if ret:
            imgOutput = cv2.warpPerspective(frame, persp, size)        
            points = get_target_points(imgOutput, lower, upper)
            if points:
                frames_no_found = 0
                last_points = points
            else:
                frames_no_found += 1
                points = last_points
        print(frames_no_found)#10 is not found

if __name__ == "__main__":
    main()