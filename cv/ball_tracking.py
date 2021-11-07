# CV

# A_x_mm = 0
# A_y_mm = 0
# B_x_mm = 233
# B_y_mm = 0
# C_x_mm = 65.4
# C_y_mm = 254.2
# D_x_mm = 139.1
# D_y_mm = 258.5
# a_x_px = 35
# a_y_px = 26
# b_x_px = 586
# b_y_px = 39
# c_x_px = 39
# c_y_px = 432
# d_x_px = 591
# d_y_px = 443
# a_r_px = 9
# b_r_px = 9
# c_r_px = 27
# d_r_px = 26

from imutils.video import VideoStream
import imutils
import cv2
import numpy
import json

vs = VideoStream(src=0).start()

maxBrightnessDiff = 13
minRadius = 4

avgCount = 40
avgSize = numpy.zeros(avgCount)
avgI = 0

def showDebug(img, point):
    debug = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)

    if point:
        cv2.circle(debug, (point['x'], point['y']), point['radius'], (255, 0, 0), 2)

    cv2.imshow('debug', debug)

    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        return True
    
    return False

while True:
    img = cv2.cvtColor(vs.read(), cv2.COLOR_BGR2GRAY)

    _, maxVal, _, _ = cv2.minMaxLoc(img)
    mask = cv2.inRange(img, maxVal - maxBrightnessDiff, maxVal)
    cnts = imutils.grab_contours(cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE))
    
    point = None
    if len(cnts) > 0:
        ((xDouble, yDouble), instantRadius) = cv2.minEnclosingCircle(max(cnts, key=cv2.contourArea))
        
        if instantRadius > minRadius:
            avgI = (avgI + 1) % avgCount
            avgSize[avgI] = int(instantRadius)

            point = {'x': int(xDouble), 'y': int(yDouble), 'radius': int(numpy.average(avgSize))}

    if point:
        print(json.dumps(point))
    
    if showDebug(img, point):
        break
