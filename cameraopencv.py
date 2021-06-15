import cv2
import numpy as np



# GREENMIN - very good //72.137.75
# GREENMAX103.255.255


def getMarkersPoints(cap):
    lower_green = np.array([72, 137, 75])
    upper_green = np.array([103, 255, 255])
    #For color test
    #createTrackbars()
    points = []
    while True:    
        _, frame = cap.read()
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv_frame, lower_green, upper_green)
        contrast_image = cv2.bitwise_and(frame, frame, mask=mask)
        #for color testing
        # cv2.imshow("mask", contrast_image)
        # lower_green, upper_green = getColorRange()
        imgBlur = cv2.GaussianBlur(contrast_image,(3, 3),1)
        imgCanny = cv2.Canny(imgBlur,50,50)
        # cv2.imshow("imgcanny", contrast_image) 
        contours,hierarchy = cv2.findContours(imgCanny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
        marker_count = 0
        points = []
        for cnt in contours:
            area = cv2.contourArea(cnt)
            # print(area)
            if area>1000:#papugai
                marker_count += 1
                cv2.drawContours(frame, cnt, -1, (255, 0, 0), 3)
                perimetr =  cv2.arcLength(cnt, True)
                approx = cv2.approxPolyDP(cnt,0.02*perimetr,True)
                x, y, w, h = cv2.boundingRect(approx)
                points.append([x+w//2, y+h//2])
        if marker_count == 4: #2 markers spotted
            break
        # print(marker_count)
        # cv2.imshow("frame + contur", frame)
        
        if cv2.waitKey(10) == 27:#ESC key
            break
    return points

def calcPerspective(marker3points,width,height):
    marker3points.sort()

    pts1 = np.float32([
        [marker3points[1] ],
        [marker3points[3] ],
        [marker3points[0] ],
        [marker3points[2] ]
    ])
    pts2 = np.float32([[0,0],[width,0],[0,height],[width,height]])
    return cv2.getPerspectiveTransform(pts1,pts2)
    
        
    pass


def main():
    cap = cv2.VideoCapture(2)
    while True:
        marker_points = getMarkersPoints(cap)
        _, frame = cap.read()
        # print(frame.size())
        for point in marker_points:
            # print(point)
            cv2.circle(frame, (point[0], point[1]), 10, (255, 0, 0), cv2.FILLED)
        # cv2.imshow("vau", frame)
        print(marker_points)
        width,height = 335,290
        matrix = calcPerspective(marker_points,width,height)

        imgOutput = cv2.warpPerspective(frame,matrix,(width,height))
        
        cv2.imshow("Output",imgOutput)

        if cv2.waitKey(10) == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()