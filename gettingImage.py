import matplotlib.pyplot as plt
import numpy as np
import cv2 as cv
import time

video = cv.VideoCapture(0)
while(video.isOpened()):
    ret, frame = video.read()
    if ret:
        cv.imshow("Cámara web", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
video.release()
cv.destroyAllWindows()
