import cv2
import time


# Title Screen
cv2.namedWindow("window", cv2.WINDOW_NORMAL);
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

photo = cv2.imread('Screen/smartBmi.png')
cv2.imshow("window", photo)
key = cv2.waitKey(1)

height = 0
for x in range (5):
    height+=1
    time.sleep(1)
    if height == 4:
        cv2.destroyAllWindows()
        break


# Stand Straight
cv2.namedWindow("window", cv2.WINDOW_NORMAL);
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

photo = cv2.imread('Screen/standStraight.png')
cv2.imshow("window", photo)
key = cv2.waitKey(2)

process = 0
for x in range (5):
    process+=1
    time.sleep(1)
    if process == 4:
        cv2.destroyAllWindows()
        break
    
    
# Processing
cv2.namedWindow("window", cv2.WINDOW_NORMAL);
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

photo = cv2.imread('Screen/processing.png')
cv2.imshow("window", photo)
key = cv2.waitKey(2)

process = 0
for x in range (5):
    process+=1
    time.sleep(1)
    if process == 4:
        cv2.destroyAllWindows()
        break
    
    
# Underweight   
#cv2.namedWindow('image3', cv2.WINDOW_NORMAL)
cv2.namedWindow("window", cv2.WINDOW_NORMAL);
cv2.setWindowProperty("window", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN);

photo = cv2.imread('Screen/underweight.png')
cv2.imshow("window", photo)
key = cv2.waitKey()