import cv2
import numpy as np
import config


def main():
    cap = cv2.VideoCapture(2)
    persp, size, suc = config.get_perspective()
    if not suc:
        print("there is no perspective")
        return
    while True:
        _, frame = cap.read() 
        imgOutput = cv2.warpPerspective(frame, persp, size)
        cv2.imshow("Output",imgOutput)

        if cv2.waitKey(10) == 27:
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()