import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture

wincap = WindowCapture('Visual Studio Code')

loop_time = time()

while (True):

    #for testing purposes use a screenshot
    screenshot = wincap.get_screenshot()
    cv.imshow('Computer Vision', screenshot)
    
    print('FPS: {}'.format( 1 / (time() - loop_time)))
    loop_time = time()

    #use q key to exit
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')