import time

import pyautogui
import cv2
import keyboard
import win32api, win32con
from PIL import Image, ImageGrab

y_adjust = 64
pyautogui.MINIMUM_SLEEP = 0
pyautogui.MINIMUM_DURATION = 0
def take_screenshot():
    myScreenshot = ImageGrab.grab()
    return myScreenshot

def mouse_action(x,y):
    pyautogui.moveTo(0, 0)
    x_offset, y_offset = pyautogui.position()
    y_offset -= y_adjust # i have uneven monitors
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x - x_offset - round(((x - x_offset) * 0.4)),
                         y - y_offset - round(((y - y_offset) * 0.4)), 0, 0)

    time.sleep(0.005)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x - x_offset - round(((x - x_offset) * 0.4)),
                         y - y_offset - round(((y - y_offset) * 0.4)), 0, 0)

    time.sleep(0.0005)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x - x_offset - round(((x - x_offset) * 0.4)),
                         y - y_offset - round(((y - y_offset) * 0.4)), 0, 0)

def detect_color(rgb):
    bot = True
    while bot:
        if keyboard.is_pressed('capslock'):
            print("Color bot shutting down!")
            exit()
        img = take_screenshot()
        #img = Image.open(filename)
        w, h = img.size
        img = img.convert('RGBA')
        data = img.getdata()
        #image = cv2.imread(filename)
        i = 0
        for item in data:
            #print(item)
            if item[0] > rgb[0] - 10 and item[1] > rgb[1] - 50 and item[2] > rgb[2] - 10:
                if item[0] < rgb[0] + 10 and item[1] < rgb[1] + 54 and item[2] < rgb[2] + 50:
                    #print(True)
                    #print("index:", [i])
                    #print("img height:", h, "| img width:", w)
                    #print("row:", i/w, "column:", (i/w % 1)*w)
                    y = round(i/w)
                    x = round((i/w % 1)*w)
                    mouse_action(x, y)
                    #image = cv2.rectangle(image, pt1=(x - 2, y - 2), pt2=(x + 2, y + 2), color=(0, 0, 0), thickness=1)
                    #cv2.imwrite("textshot.png", image)

                    break
            i += 1


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    time.sleep(5)
    detect_color((22, 201, 208)) # aim lab blue ball

