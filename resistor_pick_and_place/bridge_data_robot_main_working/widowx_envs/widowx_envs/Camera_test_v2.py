import cv2


cap = cv2.VideoCapture(4)


if not cap.isOpened():
   print("Cannot open camera")
   exit()
while True:
   ret, frame = cap.read()
   cv2.imshow('Live Feed', frame)
   cv2.waitKey(1)
