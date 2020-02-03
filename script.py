import pygame
import os, sys, math, time, random
from pygame.locals import *

PD_PORT_DIR = os.path.abspath('')+"/test"
MAX_PITCH = 70
MIN_PITCH = 50
MAX_VOL = 100
MIN_VOL = 70

def normalize(n, nmax, nmin):
    if n>nmax or n<nmin: n=nmin
    return (n-nmin)/(nmax-nmin)


SNEK_SIZE = 5
APPLE_SIZE = 10
WINDOW_SIZE = 600

def collide(x1, x2, y1, y2, w1, w2, h1, h2):
    if x1 + w1 > x2 and x1 < x2 + w2 and y1 + h1 > y2 and y1 < y2 + h2:
        return True
    else:
        return False

def die(screen, score):
    f = pygame.font.SysFont('Arial', 30)
    t = f.render('Your score was: ' + str(score), True, (0, 0, 0))
    screen.blit(t, (10, 270))
    pygame.display.update()
    pygame.time.wait(2000)
    print('Your score was: ' + str(score))
    sys.exit(0)

# snek initally five blocks long, starts from x=290
start_x = 290
start_l = 5
xs = [start_x for _ in range(start_l)]
ys = [start_x - i * SNEK_SIZE for i in range(start_l)]

dirs = 0  # 0:down  1:right  2:up  3:left
score = 0
applepos = (random.randint(0, WINDOW_SIZE - 10),
            random.randint(0, WINDOW_SIZE - 10))

pygame.init()
s = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))  # window
pygame.display.set_caption('SoundSNEK')

appleimage = pygame.Surface((APPLE_SIZE, APPLE_SIZE))
appleimage.fill((56, 112, 30))

img = pygame.Surface((SNEK_SIZE, SNEK_SIZE))
img.fill((35, 71, 168))

f = pygame.font.SysFont('Arial', 20)
clock = pygame.time.Clock()

mtime_last = 0

while True:

    clock.tick(10)

    mtime_cur = round(os.path.getmtime(PD_PORT_DIR), 3)
    if mtime_cur != mtime_last:
        with open(PD_PORT_DIR, 'r') as portf:
            line = [int(float(s)) for s in portf.readline().split()]
            if line:
                pitch = normalize(line[0], MAX_PITCH, MIN_PITCH)
                volume = normalize(line[1], MAX_VOL, MIN_VOL)
    mtime_last = mtime_cur

    if pitch!=0 and pitch!=1:
        new_dirs = int(pitch*4)
        if new_dirs-2!=dirs and new_dirs+2!=dirs:
            dirs = new_dirs
    print(mtime_cur, pitch, volume, dirs)

    pygame.event.get()
    #     if e.type == QUIT:
    #         sys.exit(0)
    #     elif e.type == KEYDOWN:
    #         if e.key == K_UP and dirs != 0: dirs = 2
    #         elif e.key == K_DOWN and dirs != 2: dirs = 0
    #         elif e.key == K_LEFT and dirs != 1: dirs = 3
    #         elif e.key == K_RIGHT and dirs != 3: dirs = 1


    # if snek bites itself
    i = len(xs) - 1
    while i >= 2:
        if collide(xs[0], xs[i], ys[0], ys[i],
        SNEK_SIZE, SNEK_SIZE, SNEK_SIZE, SNEK_SIZE):
            die(s, score)
        i -= 1

    # if snek eats apple
    if collide(xs[0], applepos[0], ys[0], applepos[1], SNEK_SIZE, 10, SNEK_SIZE, 10):
        score += 1
        xs.append(WINDOW_SIZE+100)
        ys.append(WINDOW_SIZE+100)
        applepos = (random.randint(0,WINDOW_SIZE-10),random.randint(0,WINDOW_SIZE-10))

    # if snek touch wall
    if xs[0] < 0 or xs[0] > WINDOW_SIZE-SNEK_SIZE or ys[0] < 0 or ys[0] > WINDOW_SIZE-SNEK_SIZE:
        die(s, score)

    # snek moves
    i = len(xs)-1
    while i >= 1:
        xs[i] = xs[i-1]
        ys[i] = ys[i-1]
        i -= 1
    if dirs == 0:ys[0] += SNEK_SIZE
    elif dirs == 1:xs[0] += SNEK_SIZE
    elif dirs == 2:ys[0] -= SNEK_SIZE
    elif dirs == 3:xs[0] -= SNEK_SIZE

    s.fill((255, 255, 255))
    for i in range(0, len(xs)): # render snek
        s.blit(img, (xs[i], ys[i]))

    # render apple and score
    s.blit(appleimage, applepos)
    t = f.render(str(dirs), True, (0, 0, 0))
    s.blit(t, (10, 10))

    pygame.display.update()
