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

img = cv2.imread("Satori3.png", cv2.IMREAD_COLOR)
for k in range(3):
    img[:,:,k] = scipy.ndimage.gaussian_filter(img[:,:,k],0.1)
img = cv2.cvtColor(img, cv2.COLOR_BGR2HLS)
img2 = numpy.copy(img)

visited = numpy.zeros((img.shape[0],img.shape[1]))
cv2.waitKey(0)
colors = numpy.array([
[ 288 , 48 ],
[ 398 , 59 ],
[ 392 , 40 ],
[ 352 , 82 ],
[ 491 , 126 ],
[ 541 , 152 ],
[ 534 , 185 ],
[ 541 , 218 ],
[ 498 , 223 ],
[ 372 , 114 ],
[ 466 , 149 ],
[ 503 , 168 ],
[ 519 , 271 ],
[ 470 , 235 ],
[ 336 , 199 ],
[ 180 , 156 ],
[ 139 , 297 ],
[ 206 , 423 ],
[ 177 , 453 ],
[ 259 , 451 ],
[ 229 , 341 ],
[ 219 , 339 ],
[ 216 , 310 ],
[ 339 , 293 ],
[ 354 , 292 ],
[ 406 , 316 ],
[ 400 , 286 ],
[ 195 , 352 ],
[ 203 , 359 ],
[ 200 , 370 ],
[ 236 , 357 ],
[ 407 , 333 ],
[ 427 , 337 ],
[ 206 , 375 ],
[ 446 , 350 ],
[ 370 , 369 ],
[ 223 , 376 ],
[ 368 , 359 ],
[ 229 , 393 ],
[ 238 , 374 ],
[ 244 , 389 ],
[ 262 , 398 ],
[ 259 , 384 ],
[ 391 , 367 ],
[ 406 , 361 ],
[ 406 , 380 ],
[ 436 , 359 ],
[ 508 , 502 ],
[ 533 , 496 ],
[ 544 , 493 ],
[ 308 , 540 ],
[ 268 , 532 ],
[ 230 , 537 ],
[ 367 , 623 ],
[ 339 , 530 ],
[ 307 , 579 ],
[ 294 , 611 ],
[ 258 , 604 ],
[ 280 , 566 ],
[ 601 , 350 ],
[ 574 , 477 ],
[ 550 , 472 ],
[ 547 , 518 ],
[ 525 , 526 ],
[ 517 , 529 ],
[ 566 , 129 ],
[ 576 , 68 ],
[ 596 , 217 ],
[ 581 , 230 ],
[ 568 , 613 ],
[ 147 , 607 ],
[ 273 , 546 ],
[ 305 , 558 ],
[ 335 , 565 ],
[ 359 , 540 ],
[ 398 , 520 ],
[ 396 , 571 ],
[ 445 , 532 ],
[ 486 , 598 ],
[ 568 , 610 ],
[ 594 , 601 ],
[ 607 , 599 ],
[ 516 , 634 ],
[ 617 , 625 ],
[ 581 , 636 ],
[ 623 , 639 ],
[ 544 , 640 ],
[ 448 , 325 ],
[ 452 , 365 ],
[ 449 , 339 ],
[ 446 , 333 ],
[ 430 , 356 ],
[ 430 , 369 ],
[ 233 , 609 ],
[ 278 , 628 ],
[ 293 , 631 ],
[ 527 , 221 ],
[ 535 , 240 ],
[ 551 , 328 ],
[ 591 , 405 ],
[ 580 , 444 ],
[ 552 , 452 ],
[ 539 , 336 ],
[ 591 , 296 ],
[ 574 , 263 ],
[ 609 , 407 ],
[ 622 , 500 ],
[ 669 , 595 ],
[ 650 , 536 ],
[ 617 , 555 ],
[ 246 , 561 ],
[ 222 , 580 ],
[ 296 , 549 ],
[ 280 , 548 ],
[ 206 , 595 ],
[ 185 , 613 ],
[ 173 , 636 ],
[ 158 , 649 ],
[ 647 , 649 ],
[ 641 , 654 ],
[ 666 , 648 ],
[ 497 , 623 ],
[ 309 , 654 ],
[ 290 , 654 ],
[ 155 , 653 ],
[ 348 , 582 ],
[ 315 , 600 ],
[ 326 , 604 ],
[ 353 , 586 ],
[ 373 , 553 ],
[ 217 , 494 ],
[ 250 , 526 ],
[ 273 , 519 ],
[ 291 , 529 ],
[ 298 , 528 ],
[ 296 , 549 ],
[ 314 , 532 ],
[ 319 , 531 ],
[ 128 , 398 ],
[ 149 , 414 ],
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
