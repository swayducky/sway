from PIL import ImageGrab
import pytesseract
import time
import Quartz
from AppKit import NSRunningApplication, NSWorkspace

def get_active_window_title():
    options = Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements
    window_list = Quartz.CGWindowListCopyWindowInfo(options, Quartz.kCGNullWindowID)
    active_app_pid = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationProcessIdentifier']
    active_app_windows = [window for window in window_list if window['kCGWindowOwnerPID'] == active_app_pid]

    for window in active_app_windows:
        if 'kCGWindowName' in window:
            return window['kCGWindowName']

    return None

def screenshot_ocr():

    # Take a screenshot
    screenshot = ImageGrab.grab()

    # Run OCR on the image
    text = pytesseract.image_to_string(screenshot)
    # screenshot.save('screenshot.png')

    # Print the detected text
    print(text)

while True:
    active_app = NSWorkspace.sharedWorkspace().activeApplication()['NSApplicationName']
    active_window_title = get_active_window_title()
    print("Active app:", active_app)
    if active_window_title:
        print("Active window title:", active_window_title)
    else:
        print("No active window title found")
    screenshot_ocr()
    time.sleep(1.0)