import threading
import time

import numpy as np
import cv2
import keyboard
import win32api, win32con
from PIL import Image, ImageGrab
from scipy import spatial

y_adjust = 0 #50
x_adjust = 0 #80

def take_screenshot(name='screenshot.jpg'):
    im = ImageGrab.grab()  # left , top , right, bottom
    im.save(name)
    #im.close()

def mouse_action(x,y):
    x_offset, y_offset = win32api.GetCursorPos()
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, x - x_offset - round(((x - x_offset) * 0.35)),
                         y - y_offset - round(((y - y_offset) * 0.35)), 0, 0)

    time.sleep(0.00001)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x - x_offset - round(((x - x_offset) * 0.35)),
                         y - y_offset - round(((y - y_offset) * 0.35)), 0, 0)

    time.sleep(0.0191)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x - x_offset - round(((x - x_offset) * 0.35)),
                         y - y_offset - round(((y - y_offset) * 0.35)), 0, 0)


def close_script():
    global bot
    bot = True
    while bot:
        if keyboard.is_pressed('capslock'):
            bot = False
            print("Color bot shutting down!")
            exit()
        time.sleep(1)
def detect_color(size=1):
    global bot
    bot = True
    while bot:
        take_screenshot()
        image = cv2.imread('screenshot.jpg')

        # define the list of boundaries
        # B, G, R
        close_points = []
        # loop over the boundaries
        #lower = red[0]
        #upper = red[1]
        # create NumPy arrays from the boundaries
        lower = np.array([160, 140, 0], dtype="uint8")
        upper = np.array([255, 255, 45], dtype="uint8")
        # find the colors within the specified boundaries and apply
        # the mask
        mask = cv2.inRange(image, lower, upper)
        #output = cv2.bitwise_and(image, image, mask=mask)
        #cv2.imwrite("res1.png", np.hstack([image, output]))
        ret, thresh = cv2.threshold(mask, 40, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        #contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnt = contours
        # cv2.drawContours(image, cnt, -1, (0, 255, 0), 2, cv2.LINE_AA)
        for c in cnt:
            if cv2.contourArea(c) > size:
                # print(cv2.pointPolygonTest(c, pt, True))
                # close_poly.append(cv2.pointPolygonTest(c, pt, True))
                x1, y1, w1, h1 = cv2.boundingRect(c)
                # print((x1 + (w1 / 2)), (y1 + (h1 / 2)))
                close_points.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 2))))
        # cv2.imwrite('res_marked.png', image)
        # print("closest point:", min(close_poly))
        if len(contours) != 0:
            pt = win32api.GetCursorPos()
            closest = close_points[spatial.KDTree(close_points).query(pt)[1]]
            #print(closest)
            mouse_action(closest[0], closest[1])


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting aimbot!!!")
    time.sleep(5)
    threading.Thread(target=close_script).start()
    print("Aimbot On!!!")
    detect_color() # aim lab blue ball

