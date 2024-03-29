import math
import threading
import time

import numpy as np
import cv2
import keyboard
import serial
import win32api, win32con
from PIL import Image, ImageGrab
import scipy

import PyArduinoBot_v2
from PyArduinoBot_v2 import arduino_mouse

#get the Screen resolution.
scalex = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scaley = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

PyArduinoBot_v2.FOV = 1.2 #1.04 57.2% > 1.05
PyArduinoBot_v2.FPS = True
#print("monitor scale:", scalex,scaley)

def take_screenshot(name='screenshot.jpg'):
    im = ImageGrab.grab()  # left , top , right, bottom
    im.save(name)
    im.close()


def adjust_to_fov():
    if keyboard.is_pressed(','):
        PyArduinoBot_v2.FOV += 0.01
        print(PyArduinoBot_v2.FOV, "Increasing FOV adjuster!!!")
    if keyboard.is_pressed('.'):
        PyArduinoBot_v2.FOV -= 0.01
        print(PyArduinoBot_v2.FOV, "Lowering FOV adjuster!!!")

def close_script():
    global bot
    bot = True
    while bot:
        adjust_to_fov()
        if keyboard.is_pressed('capslock'):
            bot = False
            print("Color bot shutting down!")
            exit()
        time.sleep(1)


def mouse_action(x,y, button):
    global fov, arduino
    #print("mouse action:", x,y)
    #print("adjusted action:", adj_x, adj_y)
    #print(button)
    arduino_mouse(x, y, ard=arduino, button=button, winType='FPS')
    #time.sleep(0.05)

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
        cnt = contours
        cv2.drawContours(image, cnt, -1, (255, 0, 0), 2, cv2.LINE_AA)
        #contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for c in cnt:
            if cv2.contourArea(c) > size:

                # print(cv2.pointPolygonTest(c, pt, True))
                # close_poly.append(cv2.pointPolygonTest(c, pt, True))
                x1, y1, w1, h1 = cv2.boundingRect(c)
                # print((x1 + (w1 / 2)), (y1 + (h1 / 2)))
                close_points.append((round(x1 + (w1 / 2)), round(y1 + (h1 / 2))))

        # print("closest point:", min(close_poly))
        if len(contours) != 0:
            pt = (960, 540) # screen center and crosshair position #win32api.GetCursorPos()
            #print("pt x and y:", pt)

            closest = close_points[scipy.spatial.KDTree(close_points).query(pt)[1]]

            #print(closest)
            cv2.circle(image, (closest[0], closest[1]), radius=3, color=(0, 0, 255), thickness=-1)
            cv2.line(image, pt, (closest[0], closest[1]), (0, 255, 0), 2)
            #cv2.imwrite('res_marked.png', image)
            print("desintation:",closest[0], closest[1])
            mouse_action(closest[0], closest[1], button='left')
        #cv2.imshow("images", image)
        #cv2.waitKey(10)

            #bot = False
            # mouse_action(closest[0], closest[1], button=None)
            # if abs(pt[0]) <= abs(closest[0]+15) and abs(pt[0]) >= abs(closest[0]-15):
            #     #print(pt, closest)
            #     if abs(pt[1]) <= abs(closest[1]+15) and abs(pt[1]) >= abs(closest[1]-15):
            #         print('left click actioned')
            #         mouse_action(closest[0], closest[1],  button='left')




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    global arduino
    port = 'COM5'
    baudrate = 115200
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)
    print("Starting aimbot!!!")
    time.sleep(5)
    threading.Thread(target=close_script).start()
    print("Aimbot On!!!")
    detect_color() # aim lab blue ball
    print("done!!")

