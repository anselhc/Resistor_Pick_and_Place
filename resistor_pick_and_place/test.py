import cv2
import numpy as np
print("hello world")
img = cv2.imread('single_resistor.JPG')
x = np.ones((10, 10))

#cv2.namedWindow("Processed Image #2", cv2.WINDOW_NORMAL)
cv2.imshow("Processed Image #2", img)
cv2.waitKey(0)