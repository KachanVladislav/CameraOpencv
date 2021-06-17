import argparse
import cv2
import numpy as np
from pathlib import Path
import sys
sys.path.insert(0, './config/')
import configuration as conf


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


def get_hcv_bounds(cap):
    createTrackbars()
    if not cap.isOpened():
        print("Can't open camera")
        return
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
        if  key == 27:#Esc
            cv2.destroyAllWindows()
            return
        if key == 13:#Enter
            cv2.destroyAllWindows()
            return lower_green, upper_green


def config_set_markers_hcv_bound(cap):
    bounds = get_hcv_bounds(cap) 
    if bounds:
        lower, upper = bounds
        conf.configSetMarkersHCVBounds(lower, upper)
        return True
    return False   


def getMarkersPoints(cap, lower_hcv_bound, upper_hcv_bound):
    points = []
    try_counter = 100
    while True:    
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_hcv_bound, upper_hcv_bound)
        contrast_image = cv2.bitwise_and(frame, frame, mask=mask)
        imgBlur = cv2.GaussianBlur(contrast_image,(3, 3),1)
        imgCanny = cv2.Canny(imgBlur,50,50)
        contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        marker_count = 0
        points = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area>1000:#papugai
                marker_count += 1
                cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
                perimetr =  cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt,0.02*perimetr,True)
                x, y, w, h = cv2.boundingRect(approx)
                points.append([x+w//2, y+h//2])
        if marker_count == 4: #4 markers spotted
            break
        try_counter -= 1
        if try_counter <= 0:
            print("Can't locate marker points, check hcv bounds(also there must be 4 points)")
            return
        cv2.waitKey(50)#wait for new frame
    return points


def configSetMarkerPoints(cap):
    bounds = conf.configGetMarkersHCVBounds()
    if not bounds:
        print("HCV bouds not found")
        return False
    lower,upper = bounds
    marker_points = getMarkersPoints(cap, lower, upper)
    if marker_points:
        conf.configSetMarkerPoints(marker_points)
        print("Marker points saved")
        return True
    return False


def calcPerspective(marker_points,width,height):
    marker_points.sort()

    pts1 = np.float32([
        [marker_points[1] ],
        [marker_points[3] ],
        [marker_points[0] ],
        [marker_points[2] ]
    ])
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    return cv2.getPerspectiveTransform(pts1,pts2)


def get_perspective():
    marker_points = conf.configGetMarkerPoints()
    if not marker_points:
        return 0,0,False
    width = int(conf.configGetValue("frame_width"))
    height = int(conf.configGetValue("frame_height"))
    persp = calcPerspective(marker_points, width, height)
    return persp, (width, height), True


def open_camera():
    camnum = conf.configGetValue("camnum")
    if not camnum:
        print("Using default cameranum - 2")
        camnum = 2
    else:
        camnum = int(camnum)
    return cv2.VideoCapture(camnum)


def show_warped(cap, show_original = True):
    persp, size, exist = get_perspective()
    if not exist:
        print("There is no perspective, reset markers")
        return     
    ret, frame = cap.read()
    while ret:
        imgOutput = cv2.warpPerspective(frame, persp, size)
        if show_original:
            cv2.imshow("Origin, ESC to exit", frame)
        cv2.imshow("Warped, ESC to exit", imgOutput)
        if cv2.waitKey(10) == 27:#ESC
            break
        ret, frame = cap.read()
    cv2.destroyAllWindows()


def setTargetHCVBound(cap):
    bounds = get_hcv_bounds(cap) 
    if bounds:
        lower, upper = bounds
        conf.configSetTargetHCVBounds(lower, upper)
        return True
    return False  


def main():
    parser = argparse.ArgumentParser(description = "Configuring marker points")
    parser.add_argument("--markershcv", action="store_true")
    parser.add_argument("--markersreset", action="store_true")
    parser.add_argument("--targethcv", action="store_true")
    parser.add_argument("--show", action="store_true")
    parser.add_argument('--camnum', type=int, help='provide an integer (default: 2)')
    # parser.add_argument("--cam_chanel", action="store_true") changing cam num
    args = parser.parse_args()
    
    if args.camnum:
        conf.configSetValue("camnum", str(args.camnum))
        print("Camera num saved")
    
    cap = open_camera()
    
    if args.markershcv:
        config_set_markers_hcv_bound(cap)

    if args.markersreset:
        configSetMarkerPoints(cap)
    
    if args.targethcv:
        setTargetHCVBound(cap)

    if args.show:
        show_warped(cap)

    cap.release()
    cv2.destroyAllWindows()

if (__name__ == "__main__"):
    main()