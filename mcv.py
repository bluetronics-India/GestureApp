from cv2 import *
import numpy as np
import os

headimg = imread('head_shape.jpg')

def getContours(image):
    img_gray = cvtColor(image,COLOR_BGR2GRAY)
    (T,thresh) = threshold(img_gray, 127, 255,0)
    headimg_contours,headimg_hierarchy = findContours(thresh,2,1)

    return headimg_contours

def clamp(n):
    return sorted([0, n, 99])[1]

def vol(l): os.system("osascript -e 'set volume output volume "+str(l)+"'")

headContours = getContours(headimg)

contours_IGNORE = [headContours]

# to prevent small, unwanted contours from being created
MIN_CONTOUR_AREA = 40000
# when comparing two diff contours this is the min value to declare that the two are equal
MIN_DIFF_IN_TWO_CONTOURS = 0.3

# Constants for finding range of skin color in YCrCb
min_YCrCb = np.array([0,133,77], np.uint8) # change to uppercase
max_YCrCb = np.array([255,173,127], np.uint8)

cap = VideoCapture(0)

while( cap.isOpened() ) :

    (T,img) = cap.read()

    img = flip(img,1)

    # Convert image to YCrCb - best for skin detection
    imgYCrCb = cvtColor(img, COLOR_BGR2YCR_CB)

    # blur image to reduce noise for better contours
    blur_imgYCrCb = GaussianBlur(imgYCrCb, (29,29), 0)

    # Find region with skin tone in YCrCb image
    skinRegion = inRange(blur_imgYCrCb, min_YCrCb, max_YCrCb)

    contours, hierarchy = findContours(skinRegion, RETR_EXTERNAL, CHAIN_APPROX_SIMPLE)

    contours_drawing = np.zeros(img.shape,np.uint8)

    contours_filtered = []

    for i, c in enumerate(contours):
        #remove known but unwanted shapes
        for j in contours_IGNORE:
            diff = matchShapes(j[0],c,1,0.0)
            if diff >= MIN_DIFF_IN_TWO_CONTOURS and int(contourArea(c)) > MIN_CONTOUR_AREA:
                contours_filtered.append(c)

    # draw contours
    for i, c in enumerate(contours_filtered):
        drawContours(contours_drawing, contours_filtered, i, (255, 255, 0), 1)
        drawContours(img, contours_filtered, i, (255, 255, 0), 3)

    tracking_rect_coords=[]
    for cnt in contours_filtered:
        x,y,w,h = boundingRect(cnt)
        w,h=(100,100)
        x+=100;y+=100
        tracking_rect_coords += ((clamp((x-100)/10),(y-100)/10),)
        vol(clamp((x-100)/10))
        # print clamp(x)
        rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    print tracking_rect_coords
    # vol(tracking_rect_coords[0][0])




    # imshow('contours', contours_drawing)
    # imshow('YCrCb', imgYCrCb)
    imshow('img', img)
    # imshow('head_shape', headimg)

    #
    if waitKey(1) & 0xFF == ord('q'):
        break
