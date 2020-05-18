import numpy as np
import cv2

cap = cv2.VideoCapture(0)
# 1 = nothing where as 2 showes the back camera ?
max_corners = 15 # number of feature / points
quality_lev = 0.1 # of camera img
min_dist = 20 # max dist between features

def show_edges(img, points):
    for p in points:
        print('p', p)
        print('p ', p[0][0], p[0][1])
        img[int(p[0][1])][int(p[0][0])] = 0
    return img

def is_inside(img, point):
    if point[0]>= 0 and point[0] <= len(img[0]):
        if point[1]>= 0 and point[1] <= len(img):
            return True
    return False

def show_edges(img, points):
    for p in points:
        print('p', p)
        print('p ', p[0][0], p[0][1])
        print('p ', img[int(p[0][1])][int(p[0][0])] )
        img[int(p[0][1])][int(p[0][0])] = 254

        for i in range(-1, 2):
            for j in range(-1, 2):
                if is_inside(img, [int(i + p[0][1]), int(j + p[0][0])]):
                    img[int(i + p[0][1])][int(j + p[0][0])] = 254

    return img

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # display in gray
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #cv2.imshow('frame', gray)

    # Display the resulting frame
    #print(frame)
    #print(np.shape(frame))
    #print(type(frame))
    #print(ret)
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #print(gray)
    #print(np.shape(gray))
    #edges = np.zeros_like(gray)
    #e = np.zeros((10,2), int)
    #print(e)
    #b = []
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    edges = cv2.goodFeaturesToTrack(gray, max_corners, quality_lev, min_dist)
    #edges = cv2.Canny(frame, edges)
    #edges = cv2.canny(frame, edges, 10, 30)
    #print(gray)
    print(edges)
    print(np.shape(gray))
    cv2.imshow('frame', show_edges(gray, edges))
    #cv2.imshow('frame', frame)
    #break
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture

cap.release()
cv2.destroyAllWindows()



#import cv2

#import numpy as np
#
#cap = cv2.VideoCapture(0)
#while True:
#    ret.img = cap.read()
#    cv2.imshow('video output', img)
#    k=cv2.waitKey(10) & 0xff
#    if k==27:
#        break
#cap.release()
#cv2.destroyAllWindows()
