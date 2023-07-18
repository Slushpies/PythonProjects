import cv2 as cv
import numpy as np
import os
#import win32gui
from time import time
from windowcapture import WindowCapture

window = 'File Explorer'

#returns a list of matching windows
window = WindowCapture.match_closest_window(window)

#create WindowCapture object
#window[0] = 'GitHub Desktop'
wincap = WindowCapture(window[0])

loop_time = time()


while (True):

    screenshot = wincap.get_screenshot()
    cv.imshow('Computer Vision', screenshot)
    
    print('FPS: {}'.format( 1 / (time() - loop_time)))
    loop_time = time()

    #use q key to exit
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')