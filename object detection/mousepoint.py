import pyautogui
import time

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
while True:
    
    print("Current mouse position: " + str(pyautogui.position()))
    time.sleep(1)