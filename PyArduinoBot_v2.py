# In seconds. Any duration less than this is rounded to 0.0 to instantly move
# the mouse.
import ctypes
import math
import random
import time
import ctypes.wintypes
import serial

# Credits to: # Windows implementation of PyAutoGUI functions.
# # BSD license
# # Al Sweigart al@inventwithpython.com - https://github.com/asweigart/pyautogui
num_steps = 10
FOV = 1.0
FPS = False
# FIXES SLOW TIME.SLEEP IN WINDOWS OS
timeBeginPeriod = ctypes.windll.winmm.timeBeginPeriod #new
timeBeginPeriod(1) #new

if FPS:
    addF = (960, 540)
else:
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    addF = (cursor.x, cursor.y)
previousList = [addF]
lastList = 0,0


def linear(n):
    """
    Returns ``n``, where ``n`` is the float argument between ``0.0`` and ``1.0``. This function is for the default
    linear tween for mouse moving functions.

    This function was copied from PyTweening module, so that it can be called even if PyTweening is not installed.
    """

    # We use this function instead of pytweening.linear for the default tween function just in case pytweening couldn't be imported.
    if not 0.0 <= n <= 1.0:
        raise print("Argument must be between 0.0 and 1.0.")
    return n

def _position():
    """Returns the current xy coordinates of the mouse cursor as a two-integer
    tuple by calling the GetCursorPos() win32 function.

    Returns:
      (x, y) tuple of the current xy coordinates of the mouse cursor.
    """

    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    return (cursor.x, cursor.y)


def getPointOnLine(x1, y1, x2, y2, n):
    global FOV, num_steps
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """
    print(n)
    x = (((x2 - x1) * (1 / (num_steps)))) * FOV
    y = (((y2 - y1) * (1 / (num_steps)))) * FOV
    return (str(math.ceil(x)) + ":" + str(math.ceil(y)))

def getPoint(x1, y1, x2, y2, n):
    global FOV, num_steps
    """
    Returns an (x, y) tuple of the point that has progressed a proportion ``n`` along the line defined by the two
    ``x1``, ``y1`` and ``x2``, ``y2`` coordinates.

    This function was copied from pytweening module, so that it can be called even if PyTweening is not installed.
    """
    print(n)
    x = (((x2 - x1) * (1 / (num_steps)))) * FOV
    y = (((y2 - y1) * (1 / (num_steps)))) * FOV
    return (math.ceil(x), math.ceil(y))


def _mouseMoveDrag(x, y, tween=linear, ard=None, winType=None):
    global previousList, lastList, num_steps
    if winType == 'FPS':
        startx, starty = (960, 540)
    else:
        startx, starty = _position()

    arduino = ard
    #x = int(x) if x is not None else startx
    #y = int(y) if y is not None else starty

    # If the duration is small enough, just move the cursor there instantly.
    steps = [(x, y)]
    if FPS:
        num_steps = 10
    else:
        num_steps = 30
    #print('num_steps:', num_steps)
    #print("start:", startx, starty)
    steps = [getPointOnLine(startx, starty, x, y, tween(n / num_steps)) for n in range(num_steps + 1)]
    #print("Final Coords sent:", steps)
    # Making sure the last position is the actual destination.
    if not FPS:
        steps.pop()
        steps.pop(0)


    steps = str(steps)
    print("Final Coords sent:", steps)
    arduino.write(bytes(steps, 'utf-8'))

def getLatestStatus(ard=None):
    status = 'Nothing'
    while ard.inWaiting() > 0:
        status = ard.readline()
    return status

def arduino_mouse(x=100, y=100, ard=None, button=None, winType=None):
    #
    #print("arduino mouse is:", button)
    #if button == None:
    _mouseMoveDrag(x, y, tween=linear, ard=ard, winType=winType)
    time_start = time.time()
    stat = getLatestStatus(ard)
    print(stat)
    print(time.time() - time_start)
    if button == None:
        time.sleep(0.01)
    else:
        time.sleep(0.05)
    c = random.uniform(0.02,0.05)
    #time.sleep(0.05)
    #print("passed arduino mouse is:", button)
    if button == 'left':
        ard.write(bytes(button, 'utf-8'))
        stat = getLatestStatus(ard)
        print(stat)
        time.sleep(c)
    if button == 'right':
        ard.write(bytes(button, 'utf-8'))
        stat = getLatestStatus(ard)
        print(stat)
        time.sleep(c)


if __name__ == '__main__':
    port = 'COM5'
    baudrate = 115200
    arduino = serial.Serial(port=port, baudrate=baudrate, timeout=.1)
    time.sleep(5)
    #time.sleep(3.5)
    print('using arduino mouse to move')
    if FPS:
        addF = (960,540)
    else:
        cursor = ctypes.wintypes.POINT()
        ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
        addF = (cursor.x, cursor.y)
    print(addF)
    previousList = [addF]
    lastList = 0,0
    arduino_mouse(x=200, y=200, ard=arduino, button='right')