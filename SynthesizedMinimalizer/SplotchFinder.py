import queue
import math
import cv2
import numpy
import scipy.signal


def findSplotches(fname, canvas_size):
    fname = fname.replace('/', '\\')
    fname = fname.replace('\n', '')
    img = cv2.imread(fname, cv2.IMREAD_COLOR)
    img = cv2.Canny(img,100,200)

    i,j = img.shape
    Dist_Map = numpy.zeros((i,j,3))
    Dist_Map[:,:,0] = 2*i
    Dist_Map[:,:,1] = 2*j
    temp = math.sqrt(math.pow(2*i,2)+math.pow(2*j,2))
    Dist_Map[:,:,2] = temp

    for a in range(i):
        for b in range(j):
            if img[a,b] > 1:
                Dist_Map[a,b,:] = [0,0,0]

    for a in range(i):
        for b in range(1,j):
            temp0 = Dist_Map[a,b-1,0]
            temp1 = Dist_Map[a,b-1,1] + 1
            temp2 = math.sqrt(math.pow(temp0,2) + math.pow(temp1,2))
            if temp2 < Dist_Map[a,b,2]:
                Dist_Map[a,b,:] = [temp0,temp1,temp2]

    for b in range(j):
        for a in range(1,i):
            temp0 = Dist_Map[a-1,b,0] + 1
            temp1 = Dist_Map[a-1,b,1]
            temp2 = math.sqrt(math.pow(temp0,2) + math.pow(temp1,2))
            if temp2 < Dist_Map[a,b,2]:
                Dist_Map[a,b,:] = [temp0,temp1,temp2]

    for a in range(i):
        for b in range(j-2,-1,-1):
            temp0 = Dist_Map[a,b+1,0]
            temp1 = Dist_Map[a,b+1,1] - 1
            temp2 = math.sqrt(math.pow(temp0,2) + math.pow(temp1,2))
            if temp2 < Dist_Map[a,b,2]:
                Dist_Map[a,b,:] = [temp0,temp1,temp2]

    for b in range(j):
        for a in range(i-2,-1,-1):
            temp0 = Dist_Map[a+1,b,0] - 1
            temp1 = Dist_Map[a+1,b,1]
            temp2 = math.sqrt(math.pow(temp0,2) + math.pow(temp1,2))
            if temp2 < Dist_Map[a,b,2]:
                Dist_Map[a,b,:] = [temp0,temp1,temp2]

    visited = numpy.zeros((i,j))

    for a in range(i):
        for b in range(j):
            if Dist_Map[a,b,2] < 1:
                visited[a,b] = 1

    changeQueue = queue.Queue()
    # Dist_Map[:, :, 2] = scipy.ndimage.gaussian_filter(Dist_Map[:, :, 2], 2)
    output=""
    while numpy.any(numpy.isin(visited,0)):
        max0 = 0
        max1 = 0
        max = 0
        for a in range(i):
            for b in range(j):
                if visited[a,b] == 0 and Dist_Map[a,b,2] > max:
                    max = Dist_Map[a,b,2]
                    max0 = a
                    max1 = b
        changeQueue.put([max0,max1])
        output += "\n" + (str(int(max1*599/(j-1))) + ', ' + str(int(max0*599/(i-1))) + ', 0')
        while not changeQueue.empty():
            target = changeQueue.get()
            dim0 = target[0]
            dim1 = target[1]
            visited[dim0, dim1] = 1
            for x in range(-1,2):
                for y in range(-1,2):
                    if 0 <= dim0+x < i and 0 <= dim1+y < j and visited[dim0+x,dim1+y] == 0 and (Dist_Map[dim0,dim1,2] >= Dist_Map[dim0+x,dim1+y,2] or Dist_Map[dim0+x,dim1+y,2] > 10):
                        #print(Dist_Map[dim0 + x, dim1 + y, 2])
                        visited[dim0+x,dim1+y] = 1
                        changeQueue.put([dim0+x,dim1+y])
    return output
    # for a in range(i):
    #     for b in range(j):
    #         max = 0
    #         for x in range(-1,2):
    #             for y in range(-1,2):
    #                 if (x != 0 or y != 0) and 0 <= a+x < i and 0 <= b+y < j and Dist_Map[a+x,b+y,2] > max:
    #                     max = Dist_Map[a+x,b+y,2]
    #         if Dist_Map[a,b,2] > max:
    #             print(str(int(b*599/(j-1))) + ', ' + str(int(a*599/(i-1))) + ', 0')
    #             output[a,b] = 255
