import threading
import time

import numpy as np
import cv2
import keyboard
import win32api, win32con
from PIL import Image, ImageGrab
import scipy

#get the Screen resolution.
scalex = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
scaley = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

fov = 0.65 # Change based on Field of View


#print("monitor scale:", scalex,scaley)

def take_screenshot(name='screenshot.jpg'):
    im = ImageGrab.grab()  # left , top , right, bottom
    im.save(name)
    #im.close()

def mouse_action(x,y):
    global fov
    #print("x and y:", x, y)
    pos_x, pos_y = win32api.GetCursorPos() # need to get mouse relative position and adjust for FPS screens
    #print("Pos x and y:", pos_x,pos_y)
    dx = int(x - pos_x)
    dy = int(y - pos_y)
    #print("dx and dy:", dx, dy)

    adj_x = round((dx * fov))
    adj_y = round((dy * fov))
    #print("adjusted with resolution scale:", adj_x, adj_y)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, adj_x,
                         adj_y, 0, 0)

    time.sleep(0.00001)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, adj_x,
                         adj_y, 0, 0)

    time.sleep(0.0191)

    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, adj_x,
                         adj_y, 0, 0)

def adjust_to_fov():
    global fov
    if keyboard.is_pressed(','):
        fov += 0.05
        print(fov, "Increasing FOV adjuster!!!")
    if keyboard.is_pressed('.'):
        fov -= 0.05
        print(fov, "Lowering FOV adjuster!!!")
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
        #cv2.drawContours(image, cnt, -1, (0, 255, 0), 2, cv2.LINE_AA)
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
            pt = win32api.GetCursorPos()
            #print("pt x and y:", pt)
            closest = []
            try:
                closest = close_points[scipy.spatial.KDTree(close_points).query(pt)[1]]
            except:
                pass
            #print(closest)
            #cv2.circle(image, (closest[0], closest[1]), radius=2, color=(0, 0, 255), thickness=-1)
            #cv2.imwrite('res_marked.png', image)
            #mouse_action(closest[0], closest[1])
            #time.sleep(1)
            #print("desintation:", closest[0], closest[1])
            mouse_action(closest[0], closest[1])
            #time.sleep(1)
        #cv2.imshow("images", thresh)
        #cv2.waitKey(10)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print("Starting aimbot!!!")
    time.sleep(5)
    threading.Thread(target=close_script).start()
    print("Aimbot On!!!")
    detect_color() # aim lab blue ball
    print("done!!")

