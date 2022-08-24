
import pyautogui
import numpy as np
import cv2
import random
from PIL import Image

def detect_color(rgb, filename):
    img = Image.open(filename)
    w, h = img.size
    img = img.convert('RGBA')
    data = img.getdata()
    image = cv2.imread(filename)


    i = 0
    for item in data:
        print(item)
        if item[0] == rgb[0] and item[1] == rgb[1] and item[2] == rgb[2]:
            print(True)
            print("index:", [i])
            print("img height:", h, "| img width:", w)
            print("row:", i/w, "column:", (i/w % 1)*w)
            p2 = round(i/w)
            p1 = round((i/w % 1)*w)
            image = cv2.rectangle(image, pt1=(p1 - 2, p2 - 2), pt2=(p1 + 2, p2 + 2), color=(0, 0, 0), thickness=1)
            cv2.imwrite("textshot.png", image)
            return True
        i += 1
    print(False)
    return False



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    detect_color((255, 0, 0), 'test.png') # red
    #detect_color((0, 255, 0), 'test.png') # green
    #detect_color((0, 0, 255), 'test.png') # blue
