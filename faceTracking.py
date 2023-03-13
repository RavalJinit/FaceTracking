
from main import *
import cv2

w, h = 360, 240
pid = [0.4, 0.4, 0]
pError = 0
startCounter = 0  # for no Flight 1   - for flight 0

me = initializeTello()

while True:

    ## Flight
    if startCounter == 0:
        me.takeoff()
        startCounter = 1

    ## Step 1
    img = telloGetFrame(me, w, h)
    ## Step 2
    # img, info = findFace(img)
    # ## Step 3
    # pError = trackFace(me, info, w, pid, pError)
    # # print(info[0][0])
    cv2.imshow('Image', img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        me.land()
        break