import pyautogui
import time
import random

def mouse_jiggler():
    while True:
        try: 
            x_dist = random.randint(0,75)
            y_dist = random.randint(0,75)
            x_offset = random.randint(-x_dist, x_dist)
            y_offset = random.randint(-y_dist, y_dist)
            pyautogui.moveRel(x_offset, y_offset, duration=0.25)
            time.sleep(random.randint(.75, 2.5))

        except Exception:
            pass

if __name__ == "__main__":
    mouse_jiggler()