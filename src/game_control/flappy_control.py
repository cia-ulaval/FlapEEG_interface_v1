"""Install with pip install pyautogui."""
import pyautogui
import time

chrono = time.time()
REFRESH_JUMP_THRESHOLD = 0.1
jump_number = 0

def jump():
    """Makes flappy bird jump"""
    global chrono
    global jump_number 
    if time.time() - chrono > REFRESH_JUMP_THRESHOLD:
        pyautogui.press('up')
        chrono  = time.time()
        jump_number += 1  
