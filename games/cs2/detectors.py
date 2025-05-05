import cv2
import numpy as np
import pyautogui
import time
from pathlib import Path

# Match a template image on the screen using OpenCV
def match_template(template_path, threshold=0.8):
    if not Path(template_path).is_file():
        print(f"❌ [Error] Template not found: {template_path}")
        return None

    # Take a screenshot and convert it to a NumPy BGR image
    screen = pyautogui.screenshot()
    screen = cv2.cvtColor(np.array(screen), cv2.COLOR_RGB2BGR)

    # Load template and perform match
    template = cv2.imread(template_path)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    # Return location if match is confident enough
    if max_val >= threshold:
        print(f"✅ [Detect] Match found at {max_loc} with confidence {max_val:.2f}")
        return max_loc
    else:
        print(f"⚠️ [Detect] No match found (max confidence {max_val:.2f})")
        return None

# Wait until a template appears on screen or timeout
def wait_for_template(template_path, timeout=30, check_interval=1):
    start = time.time()
    while time.time() - start < timeout:
        if match_template(template_path):
            return True
        time.sleep(check_interval)
    return False
