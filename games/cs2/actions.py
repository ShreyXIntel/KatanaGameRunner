import pyautogui
import time
import cv2
from pathlib import Path
from .detectors import match_template

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
        pyautogui.moveTo(center_x, center_y, duration=0.25)
        pyautogui.click()
        time.sleep(click_delay)
        print(f"✅ [Click] Clicked at ({center_x}, {center_y})")
    else:
        print(f"❌ [Click] Failed to find template: {template_path}")

def click_play_tab():
    # Click on the PLAY tab on the CS2 main menu
    click_on_template(str(ASSET_DIR / "play_tab.png"))

def select_game_mode(template_filename):
    # Click on a game mode or map option using its template
    path = str(ASSET_DIR / template_filename)
    click_on_template(path)
