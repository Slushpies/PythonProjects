import cv2 as cv
import numpy as np
import os
import pyautogui
import time

loop_time = time.time()

while (True):

    #for testing purposes use a screenshot
    screenshot = pyautogui.screenshot()
    screenshot = np.array(screenshot)
    screenshot = cv.cvtColor(screenshot, cv.COLOR_RGB2BGR)
    
    cv.imshow('Computer Vision', screenshot)
    
    print('FPS: {}'.format( 1 / (time.time() - loop_time)))
    loop_time = time.time()

    #use q key to exit
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')