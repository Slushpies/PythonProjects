import win32gui
import win32ui
import win32con
import numpy as np

class WindowCapture:
    
    #screen size
    w = 0
    h = 0
    hwnd = None
    
    #constructor
    def __init__(self, window_name):
        
        self.w = 1920
        self.h = 1080
        
        self.hwnd = win32gui.FindWindow(None, window_name)
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
    
    def get_screenshot(self):
        
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj=win32ui.CreateDCFromHandle(wDC)
        cDC=dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0,0),(self.w, self.h) , dcObj, (0,0), win32con.SRCCOPY)
        
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # Free Resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())
        
        #optional remove alpha channel (transparency)
        #img = img[...,:3]
        #img = np.ascontiguousarray(img)
        
        return img