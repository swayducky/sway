import Quartz

active_app = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)[0]['kCGWindowOwnerName']

print(active_app)

import AppKit

active_app = Quartz.CGWindowListCopyWindowInfo(Quartz.kCGWindowListOptionOnScreenOnly | Quartz.kCGWindowListExcludeDesktopElements, Quartz.kCGNullWindowID)[0]['kCGWindowOwnerName']

app = AppKit.NSRunningApplication.runningApplicationWithProcessIdentifier_(int(active_app.split(' ')[0]))

text = app.activateWithOptions_(AppKit.NSApplicationActivateIgnoringOtherApps).windows[0].delegate.windowShouldClose_(None)

print(text)
