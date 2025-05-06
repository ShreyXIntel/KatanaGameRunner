"""
Simple Win32 mouse click module.
Provides a basic function for clicking at specific coordinates using Win32 API.
"""

import win32api
import win32con
import time

def win32_click(x, y, delay=0.1):
    """
    Perform a mouse click at the specified coordinates using Win32 API.
    
    Parameters:
    - x: X coordinate on screen
    - y: Y coordinate on screen
    - delay: Delay between mouse down and up events (seconds)
    
    Returns:
    - None
    """
    # Move cursor to position
    win32api.SetCursorPos((x, y))
    
    # Small delay after moving cursor
    time.sleep(0.05)
    
    # Perform left click
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(delay)  # Small delay between down and up
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)