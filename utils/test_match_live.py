
import cv2
import numpy as np
import pyautogui
import time
import sys
from pathlib import Path

def capture_screen():
    screenshot = pyautogui.screenshot()
    return cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

def match_template_live(template_path, threshold=0.5):
    screen = capture_screen()
    if not Path(template_path).is_file():
        print(f"[ERROR] Template not found: {template_path}")
        return screen

    template = cv2.imread(str(template_path), cv2.IMREAD_COLOR)
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)

    print(f"[Match] Confidence: {max_val:.2f}, Location: {max_loc}")

    if max_val >= threshold:
        h, w = template.shape[:2]
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(screen, top_left, bottom_right, (0, 255, 0), 2)
        cv2.putText(screen, f"{max_val:.2f}", (top_left[0], top_left[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    return screen

def main():
    if len(sys.argv) < 2:
        print("Usage: python test_match_live.py path/to/template.png")
        sys.exit(1)

    template_file = Path(sys.argv[1])

    while True:
        matched_screen = match_template_live(template_file)
        cv2.imshow("Live Match", matched_screen)
        if cv2.waitKey(5000) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
