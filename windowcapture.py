import win32gui
import win32ui
import win32con
import numpy as np
import difflib


class WindowCapture:
    
    #screen size
    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    
    #constructor
    def __init__(self, window_name):
        
        self.w = 1920
        self.h = 1080
        
        self.hwnd = win32gui.FindWindow(None, window_name)
        #self.hwnd = window_name
        if not self.hwnd:
            raise Exception('Window not found: {}'.format(window_name))
        
        # get the window size
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]
        
        # account for the window border and titlebar and cut them off
        border_pixels = 8
        titlebar_pixels = 30
        self.w = self.w - (border_pixels * 2)
        self.h = self.h - titlebar_pixels - border_pixels
        self.cropped_x = border_pixels
        self.cropped_y = titlebar_pixels

        # set the cropped coordinates offset so we can translate screenshot
        # images into actual screen positions
        self.offset_x = window_rect[0] + self.cropped_x
        self.offset_y = window_rect[1] + self.cropped_y
        
    @staticmethod
    def match_closest_window(window_name):
        windows = []
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible(hwnd) and window_name in win32gui.GetWindowText(hwnd):
                hex(hwnd)
                windows.append(win32gui.GetWindowText(hwnd))

        win32gui.EnumWindows( winEnumHandler, None )
        
        print("Capturing: \"{}\"".format(windows[0]))
        return windows
    
    def get_screenshot(self):

        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (self.cropped_x, self.cropped_y), win32con.SRCCOPY)

        # convert the raw data into a format opencv can read
        #dataBitMap.SaveBitmapFile(cDC, 'debug.bmp')
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.h, self.w, 4)

        # free resources
        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        #optional remove alpha
        #img = img[...,:3]
        #img = np.ascontiguousarray(img)

        return img
    
    def list_window_names(self):
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

        win32gui.EnumWindows( winEnumHandler, None )