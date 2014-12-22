from cv2 import *
import numpy as np

"""
for each contour get area and something with the greatest area is probably IMPORTANT so only that area will be
given importance to -- NEED TO TEST
"""

headimg = imread('head_shape.jpg')

def getContours(image):
    img_gray = cvtColor(image,COLOR_BGR2GRAY)
    (T,thresh) = threshold(img_gray, 127, 255,0)
    headimg_contours,headimg_hierarchy = findContours(thresh,2,1)

    return headimg_contours

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

    (T,img) = cap.read(); img = flip(img,1)

    # Convert image to YCrCb - best for skin detection
    imgYCrCb = cvtColor(img, COLOR_BGR2YCR_CB)

    # blur image to reduce noise for better contours
    blur_imgYCrCb = GaussianBlur(imgYCrCb, (29,29), 0)

    # Find region with skin tone in YCrCb image
    skinRegion = inRange(blur_imgYCrCb, min_YCrCb, max_YCrCb)

    #dialate and erode for better contours
    skinRegion = erode(skinRegion, getStructuringElement(MORPH_ELLIPSE,(29,29)))
    skinRegion = dilate(skinRegion, getStructuringElement(MORPH_ELLIPSE,(29,29)))

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
        # print "area of",i,"is:",contourArea(c)
        drawContours(contours_drawing, contours_filtered, i, (255, 255, 0), 1)
        drawContours(img, contours_filtered, i, (255, 255, 0), 3)

    for cnt in contours_filtered:

        hull = convexHull(cnt)
        drawContours(img,[hull],0,(150,55,140),2)

        M = moments(cnt) # to find center of mass
        if(M["m00"]!=0):
            c_x = int(M["m10"]/M["m00"])
            c_y = int(M["m01"]/M["m00"])
            #two circles for the cool target effect
            circle(img, (c_x,c_y), 5, (0,0,255), -1)
            circle(img, (c_x,c_y), 15, (254,0,0), 3)

        cnt = approxPolyDP(cnt,0.01*arcLength(cnt,True),True)
        hull = convexHull(cnt,returnPoints=False)
        defects = convexityDefects(cnt,hull)
        # print len(defects) # approximates num of fingers

        if len(defects) != 0:
            for i in range(defects.shape[0]):
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                # line(img,start,end,[0,255,0],2)
                circle(img,far,5,[0,0,255],-1)



    # imshow('contours', contours_drawing)
    imshow('YCrCb', blur_imgYCrCb)
    imshow('img', img)
    # imshow('skinRegion', skinRegion)

    #
    if waitKey(1) & 0xFF == ord('q'):
        break
