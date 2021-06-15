import cv2
import numpy as np
import config


def main():
    cap = cv2.VideoCapture(2)
    persp, size = config.get_perspective()

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