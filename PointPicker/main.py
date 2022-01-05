import cv2
import numpy

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('[',x,',',y,'],')


img = cv2.imread("image.jpg", cv2.IMREAD_COLOR)
cv2.imshow("output",img)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)

minimal = numpy.zeros((img.shape[0], img.shape[1]))

cv2.setMouseCallback('output', click_event)

cv2.waitKey(0)

cv2.destroyAllWindows()