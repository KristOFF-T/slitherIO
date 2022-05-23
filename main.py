import pygame as pg
from random import randint, choice
from data.functions import *
from math import *
pg.init()

print("1: controlled\n2: AI")
mode = int(input("mode: "))

screen = pg.display.set_mode((W, H), pygame.FULLSCREEN)

clock = pg.time.Clock()
FPS = 60

RS = 50
CRS = int(RS/2)
R_SPD = 15
MRAD = 3000

rects = [[[100,100,RS,RS], [0, 0]]]

pos = (CX, CY)

scroll = [0, 0]

lw = 3
c = (0,0,255)

points = []
def generate_points():
    for i in range(500):
        x = randint(-500, 500)*10
        y = randint(-500, 500)*10

        if getdist([CX,CY], [x, y]) < MRAD-50:
            c = choice([GREEN, BLUE, YELLOW, RED])
            
            points.append([[x, y], c])

enemies = []
for i in range(5):
    x = randint(1, 128)*200
    y = randint(1, 72)*2

    [[[x,y,RS,RS], [0, 0]]]

generate_points()

def ai():
    posses = []
    for p in points:
        e = hypot(p[0][1]-rects[0][0][1], p[0][0]-rects[0][0][0])
        posses.append(e)

    for p in points:
        e = hypot(p[0][1]-rects[0][0][1], p[0][0]-rects[0][0][0])
        if e == min(posses):
            global pos
            pos = p[0][0]+scroll[0], p[0][1]+scroll[1]
            return e

score = 0

run = True
while run:
    if mode == 1: pos = pg.mouse.get_pos()
    clock.tick(FPS)
    screen.fill((0,0,0))

    if mode == 2: distance = ai()
    
    for num, p in enumerate(points):
        if -RS < p[0][0]+scroll[0] < W and -RS < p[0][1]+scroll[1] < H:
            pg.draw.circle(screen, p[1], [p[0][0]+scroll[0], p[0][1]+scroll[1]], 10)

    if len(points) < 50:
        generate_points()

    for num, r in enumerate(rects):
        rect = r[0]
        if -RS < rect[0]+scroll[0] < W and -RS < rect[1]+scroll[1] < H:
            pg.draw.circle(screen, (0,120,255), (rect[0]+CRS+scroll[0], rect[1]+CRS+scroll[1]), CRS)
            if r == rects[0]:
                for pnum, p in enumerate(points):
                    if pygame.Rect(rect).collidepoint(p[0]):
                        score += 1
                        if len(rects) < 20:
                            sp = points[pnum-1]
                            lrn = len(rects)-1
                            lr = rects[lrn]
                            lrr = lr[0]
                            rects.append([ [lrr[0], lrr[1], RS, RS], [0,0] ])

                        if RS > 100:
                            RS += 1
                            CRS = int(RS/2)
                            r[0] = [r[0][0], r[0][1], RS, RS]
                        
                        if p in points:
                            points.remove(p)

            else:
                pr = rects[num-1][0]
                sx = scroll[0]
                sy = scroll[1]

    # eyes
    r = rects[0]
    pygame.draw.circle(screen, WHITE, (r[0][0]+CRS+scroll[0]-(int(CRS/2))-r[1][0], r[0][1]+CRS+scroll[1]-r[1][1]*2), int(CRS/4))
    pygame.draw.circle(screen, WHITE, (r[0][0]+CRS+scroll[0]+(int(CRS/2))-r[1][0], r[0][1]+CRS+scroll[1]-r[1][1]*2), int(CRS/4))

    if getdist(r[0], [CX, CY]) > MRAD:
       run = False

    pygame.draw.circle(screen, RED, (scroll[0]+CX, scroll[1]+CY), MRAD, 10)

    mts(screen, False, 30, f'score: {score}', WHITE, 20, 20)
    if mode == 2:
       mts(screen, False, 30, f'dist: {int(distance)}px', WHITE, 20, 70)

    pg.display.update()

    for num, r in enumerate(rects):
        if num == 0: target = (pos[0]-CRS-scroll[0], pos[1]-CRS-scroll[1])

        else:
            e = rects[num-1]
            target = (e[0][0]+e[1][0]-r[1][0], e[0][1]+e[1][1]-r[1][1])
        
        radians = atan2(r[0][1]-target[1], r[0][0]-target[0])

        dx = cos(radians)*R_SPD
        dy = sin(radians)*R_SPD

        r[1][0] = dx
        r[1][1] = dy

        if hypot(target[1]-r[0][1], target[0]-r[0][0]) > RS or num == 0:
            r[0][0] -= r[1][0]
            r[0][1] -= r[1][1]

    scroll[0] = -rects[0][0][0]+CX-CRS
    scroll[1] = -rects[0][0][1]+CY-CRS
    
    for ev in pg.event.get():
        if ev.type == pg.QUIT:
            run = False

pg.quit()
