# Python code to read image
import heapq
import math
import cv2
import matplotlib.pyplot as plt
import numpy
import scipy.signal

class ChangeRequest:

    def __init__(self, x, y, val, priority):
        self.priority = priority
        self.x = x
        self.y = y
        self.val = val

    def __repr__(self):
        return str(self.priority)

    def __lt__(self, other):
        return self.priority < other.priority


class ChangeRequestQueue:
    queue = []

    def __init__(self, CRs):
        for i in range(len(CRs)):
            self.push(CRs[i])

    def push(self, CR):
        heapq.heappush(self.queue,CR)

    def pop(self):
        return heapq.heappop(self.queue)

    def __len__(self):
        return len(self.queue)



def HLSDist(val1, val2):
    val1x = (abs(abs(val1[1] - 128) - 128) / 128) * (val1[2] / 255) * math.cos(val1[0] * math.pi / 90)
    val1y = (abs(abs(val1[1] - 128) - 128) / 128) * (val1[2] / 255) * math.sin(val1[0] * math.pi / 90)
    val1z = (val1[1] - 128) / 128
    val2x = (abs(abs(val2[1] - 128) - 128) / 128) * (val2[2] / 255) * math.cos(val2[0] * math.pi / 90)
    val2y = (abs(abs(val2[1] - 128) - 128) / 128) * (val2[2] / 255) * math.sin(val2[0] * math.pi / 90)
    val2z = (val2[1] - 128) / 128
    return math.dist([val1x, val1y, val1z], [val2x, val2y, val2z])

img = cv2.imread("image.jpg", cv2.IMREAD_COLOR)
for k in range(3):
    img[:,:,k] = scipy.ndimage.gaussian_filter(img[:,:,k],0.1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
img2 = numpy.copy(img)

visited = numpy.zeros((img.shape[0],img.shape[1]))
cv2.waitKey(0)
colors = numpy.array([

])
temp = numpy.copy(colors[:,0])
colors[:,0] = colors[:,1]
colors[:,1] = temp
CRQ = ChangeRequestQueue(())

for i in range(colors.shape[0]):
    CRQ.push(ChangeRequest(colors[i,0],colors[i,1],img[colors[i,0],colors[i,1],:],0))

while len(CRQ) != 0:
    target = CRQ.pop()
    if visited[target.x,target.y] == 0:
        visited[target.x,target.y] = 1
        img2[target.x,target.y,:] = target.val
        for i,j in [(-1,0),(0,-1),(0,1),(1,0)]:
                if target.x + i >= 0 and target.x + i < visited.shape[0] and target.y + j >= 0 and target.y + j < visited.shape[1] and visited[target.x + i, target.y + j] == 0:
                    CRQ.push(ChangeRequest(target.x + i, target.y + j, target.val,
                                           HLSDist(target.val, img[target.x + i, target.y + j])))

img = img2
img = cv2.cvtColor(img, cv2.COLOR_HLS2BGR)
cv2.imshow("Image", img)
cv2.imwrite("minimalistimage.png",img)
cv2.waitKey(0)
cv2.destroyAllWindows()
