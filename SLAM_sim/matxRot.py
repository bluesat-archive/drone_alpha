import pygame
import math
import numpy as np


pygame.init()
gray = (115, 115, 115)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)
lightGreen = (155, 255, 0)
yellow = (255, 255, 0)
white = (255, 255, 255)

display_width = 900
display_height = 900

width = 10
height = width
pos_xy = [10, 10]
points = []
clock = pygame.time.Clock()
gameDisplay = pygame.display.set_mode((display_width, display_height))
FPS = 30

# focus point behind the camera
zc = 350



def matxmul(pos, rot):
    #matx = np.ones
    # this should rotate pi/2 clockwise
    matx = [[1, -1],[1, 1]]
    np.multiply([x, y], matx)


def rotate(pos, screenCentre, rot):
    print("rotating")
    thetha = rot[0]*2*math.pi /100
    pos[0] = (pos[0]*math.cos(thetha)) - (pos[1]*math.sin(thetha))
    pos[1] = (pos[0]*math.sin(thetha)) + (pos[1]*math.cos(thetha))

    thetha = rot[1]*2*math.pi /100
    pos[0] = (pos[0]*math.cos(thetha)) - (pos[2]*math.sin(thetha))
    pos[2] = (pos[0]*math.sin(thetha)) + (pos[2]*math.cos(thetha))

    thetha = rot[2]*2*math.pi /100
    pos[2] = (pos[2]*math.cos(thetha)) - (pos[1]*math.sin(thetha))
    pos[1] = (pos[2]*math.sin(thetha)) + (pos[1]*math.cos(thetha))

    #pos[0] = (pos[0]*math.sin(thetha)) - (pos[1]*math.cos(thetha))
    #pos[1] = (pos[0]*math.cos(thetha)) + (pos[1]*math.sin(thetha))
    #pos[0] = (pos[0]/math.sqrt(((pos[0])*(pos[0])) + ((pos[1])*(pos[1])))
    #pos[0] = math.sin(math.pi * rot[0]) + math.cos(math.pi * rot[0])
    #pos[1] = -math.cos(math.pi * rot[0]) + math.sin(math.pi * rot[0])
    #pos[0] = math.sin(math.pi * rot)
    #rot = [0, 0, 0]

#def display2Screen(gameDisplay):

def to2D(d3):
    # takes in a 3d point and returns a 2d point
    #d3 = [d3[0]+(display_width//2), d3[1]+(display_width//2)]

    #p1 = zc* d3[0] /d3[2]
    #p2 = zc* d3[1] /d3[2]
    #return p1+(display_width//2), p2+(display_width//2)
    return zc* d3[0] /(zc+d3[2]), zc* d3[1] /(zc+d3[2])



def displayPoints(points):
    for p in points :
        if (p[2] > 0):
            x, y = to2D(p)
            x += display_width/2
            y += display_width/2
            x = round(x)
            y = round(y)
            x = int(x)
            y = int(y)
            #x = int(math.roof(x))
            #y = int(math.roof(y))
            #pygame.draw.circle(gameDisplay, red, [x, y, 5] )
            print("point")
            print(x, y)
            dist = math.sqrt((p[0]**2) + (p[1]**2) + (p[2]**2))
            Psize = (display_width - dist) // 90
            if (Psize <1) :
                Psize =1
            Psize = int(Psize)
            pygame.draw.circle(gameDisplay, green, [x, y], Psize)
            #pygame.draw.rect(gameDisplay, red, [pos[0], pos[1], size[0], size[1]] )


def gameLoop():
    matx = np.random.randint(10, size =(3))
    print('matx = ')
    #print("matx = %" %(matx))
    print(matx)
    gameDisplay.fill(gray)
    gameExit = False

    for i in range(100):
        points.append(np.random.randint(-display_width//2, display_width//2, size = (3)))
        points[i][2] = math.fabs(points[i][2])


    print("points")
    print(points)

    pos = [50, 50, 50]
    size = [150, 150, 150]
    rot = [0, 0, 0]

    
    while not gameExit:
        #print("adwaw")
        pygame.display.update()
        gameDisplay.fill(gray)
        displayPoints(points)
        #pygame.draw.rect(gameDisplay, red, [pos[0], pos[1], size[0], size[1]] )

        key = pygame.key.get_pressed()
        for p in points:
            #
            #rotDir = np.random.randint(-1,1,  size = (3))
            #rotate(p, size, rotDir)
            #rotate(p, size, [0, -1, 0])
            #
            speed = 4
            if (key[pygame.K_m]) :
                p[2] -= speed
            if (key[pygame.K_n]) :
                p[2] += speed
            if (key[pygame.K_UP] or key[pygame.K_w]) :
                p[1] -= speed
            if (key[pygame.K_DOWN] or key[pygame.K_s]) :
                p[1] += speed
            if (key[pygame.K_RIGHT] or key[pygame.K_d]) :
                p[0] += speed
            if (key[pygame.K_LEFT] or key[pygame.K_a]) :
                p[0] -= speed
            if (key[pygame.K_x]) :
                if (key[pygame.K_RIGHT] or key[pygame.K_d]) :
                    rotate(p, size, [0, 0, -1])
                if (key[pygame.K_LEFT] or key[pygame.K_a]) :
                    rotate(p, size, [0, 0, 1])
            if (key[pygame.K_y]) :
                if (key[pygame.K_RIGHT] or key[pygame.K_d]) :
                    rotate(p, size, [0, -1, 0])
                if (key[pygame.K_LEFT] or key[pygame.K_a]) :
                    rotate(p, size, [0, 1, 0])
            if (key[pygame.K_z]) :
                if (key[pygame.K_RIGHT] or key[pygame.K_d]) :
                    rotate(p, size, [-1, 0, 0])
                if (key[pygame.K_LEFT] or key[pygame.K_a]) :
                    rotate(p, size, [1, 0, 0])
        if key[pygame.K_q] :
            gameExit = True

        #click = pygame.mouse.get_pressed()
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameExit = True

        clock.tick(FPS)
    pygame.quit()
    quit()
gameLoop()
