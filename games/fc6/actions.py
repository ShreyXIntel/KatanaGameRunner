import pyautogui
import time
import cv2
from pathlib import Path
from detectors import match_template
from win32_mouse import win32_click

# Resolve the path to the local 'assets' folder
ASSET_DIR = Path(__file__).parent / "assets"

def click_on_template(template_path, threshold=0.8, click_delay=0.5):
    print(f"🖱️ [Click] Searching and clicking: {template_path}")
    match = match_template(template_path, threshold)
    if match:
        x, y = match
        template = cv2.imread(template_path)
        h, w = template.shape[:2]
        center_x, center_y = x + w // 2, y + h // 2
        
        # Use Win32 click instead of pyautogui
        win32_click(center_x, center_y, click_delay)
        
        print(f"✅ [Click] Clicked at ({center_x}, {center_y})")
    else:
        print(f"❌ [Click] Failed to find template: {template_path}")


def click_on_btn(btn_template):
    # Click on the Options button on the FC6 main menu
    click_on_template(str(ASSET_DIR / btn_template))

# def click_on_template(template_path, threshold=0.8, click_delay=0.5):
#     print(f"🖱️ [Click] Searching and clicking: {template_path}")
#     match = match_template(template_path, threshold)
#     if match:
#         x, y = match
#         template = cv2.imread(template_path)
#         h, w = template.shape[:2]
#         center_x, center_y = x + w // 2, y + h // 2
#         pyautogui.moveTo(center_x, center_y, duration=0.25)
#         pyautogui.click()
#         time.sleep(click_delay)
#         print(f"✅ [Click] Clicked at ({center_x}, {center_y})")
#     else:
#         print(f"❌ [Click] Failed to find template: {template_path}")