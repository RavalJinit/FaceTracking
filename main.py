import cv2
import numpy as np
from djitellopy import Tello

def initializeTello():
    me = Tello()
    me.connect()
    me.for_back_velocity = 0
    me.up_down_velocity = 0
    me.left_right_velocity = 0
    me.yaw_velocity = 0
    me.speed = 0
    print(me.get_battery())
    me.streamoff()
    me.streamon()
    return me

def telloGetFrame(me, w= 360,h=240):
    myFrame = me.get_frame_read()
    myFrame = myFrame.frame
    img = cv2.resize(myFrame,(w,h))
    return img


def findFace(img):
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(imgGray, 1.1, 6)

    myFaceListC = []
    myFaceListArea = []

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cx = x + w // 2
        cy = y + h // 2
        area = w * h
        myFaceListArea.append(area)
        myFaceListC.append([cx, cy])

    if len(myFaceListArea) != 0:
        i = myFaceListArea.index(max(myFaceListArea))
        return img, [myFaceListC[i], myFaceListArea[i]]
    else:
        return img, [[0, 0], 0]


def trackFace(me, info, w, pid, pError):
    ## PID
    error = info[0][0] - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -100, 100))

    print(speed)
    if info[0][0] != 0:
        me.yaw_velocity = speed
    else:
        me.for_back_velocity = 0
        me.left_right_velocity = 0
        me.up_down_velocity = 0
        me.yaw_velocity = 0
        error = 0
    if me.send_rc_control:
        me.send_rc_control(me.left_right_velocity,
                                me.for_back_velocity,
                                me.up_down_velocity,
                                me.yaw_velocity)
    return error