import cv2
import numpy as np
from Resistor_detector import detect_resistors

img = cv2.imread('single_resistor.JPG')
# will need to invert the image colors
#print(img)
# Generate contours
resistor_contour, binary_image = detect_resistors(img)
img = binary_image
for row in img:
    for pixel in row:
        if pixel == 1:
            pixel = 255
img = cv2.merge((img, img, img))
print(img)
# create new array which is three times the img array stacked
cv2.namedWindow("Processed Image", cv2.WINDOW_NORMAL)
cv2.imshow("Processed Image", img)
cv2.waitKey(0)

# Draw and display contours
# for i in enumerate(resistor_contour):
#     cv2.drawContours(
#         img,
#         resistor_contour,
#         i[0],cle
#         (0, 0, 255),
#         1,
#     )
# cv2.imshow("Resistor With Contours", img)

gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)


# sure background area
sure_bg = cv2.dilate(opening,kernel,iterations=3)


# Finding sure foreground area
dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
ret, sure_fg = cv2.threshold(dist_transform,0.01*dist_transform.max(),255,0)


# Finding unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)


# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)


# Add one to all labels so that sure background is not 0, but 1
markers = markers+1


# Now, mark the region of unknown with zero
markers[unknown==255] = 0


markers = cv2.watershed(img,markers)
img[markers == -1] = [255,0,0]


cv2.namedWindow("Processed Image #2", cv2.WINDOW_NORMAL)
cv2.imshow("Processed Image #2", sure_fg)
cv2.waitKey(0)
