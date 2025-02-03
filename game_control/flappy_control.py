"""Install with pip install pyautogui."""
import pyautogui

def jump():
    """Makes flappy bird jump"""
    pyautogui.press('space', interval=0.3)
    print("Jump!!")
