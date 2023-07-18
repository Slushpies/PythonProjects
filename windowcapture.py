import win32gui
import win32ui
import win32con
import numpy as np
from ctypes import windll

class WindowCapture:
    
    #screen size
    window_name = ''
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
        
        self.window_name = window_name
        
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

        windll.user32.SetProcessDPIAware()
        hwnd = win32gui.FindWindow(None, self.window_name)

        left, top, right, bottom = win32gui.GetClientRect(hwnd)
        w = right - left
        h = bottom - top

        hwnd_dc = win32gui.GetWindowDC(hwnd)
        mfc_dc = win32ui.CreateDCFromHandle(hwnd_dc)
        save_dc = mfc_dc.CreateCompatibleDC()
        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(mfc_dc, w, h)
        save_dc.SelectObject(bitmap)

        # If Special K is running, this number is 3. If not, 1
        result = windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 3)

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        img = np.frombuffer(bmpstr, dtype=np.uint8).reshape((bmpinfo["bmHeight"], bmpinfo["bmWidth"], 4))
        img = np.ascontiguousarray(img)[..., :-1]  # make image C_CONTIGUOUS and drop alpha channel

        if not result:  # result should be 1
            win32gui.DeleteObject(bitmap.GetHandle())
            save_dc.DeleteDC()
            mfc_dc.DeleteDC()
            win32gui.ReleaseDC(hwnd, hwnd_dc)
            raise RuntimeError(f"Unable to acquire screenshot! Result: {result}")

        return img
    
    def list_window_names(self):
        def winEnumHandler( hwnd, ctx ):
            if win32gui.IsWindowVisible( hwnd ):
                print ( hex( hwnd ), win32gui.GetWindowText( hwnd ) )

        win32gui.EnumWindows( winEnumHandler, None )