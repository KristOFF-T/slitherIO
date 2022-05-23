import pygame
pygame.font.init()

W = 1280
H = 720
CX = int(W/2)
CY = int(H/2)

def getdist(p1, p2):
   w = abs(p1[0]-p2[0])
   h = abs(p1[1]-p2[1])
   dist = (w**2 + h**2) ** 0.5
   return dist

def font(size):
    font = pygame.font.Font('data/FFFFORWA.TTF', size)
    return font

def mts(surface, rect, size, smthing, color, x, y):
    text = font(size).render(smthing, 1, color)
    if rect:
        text_rect = text.get_rect(center = (x, y))
        surface.blit((text), text_rect)
    elif not rect:
        surface.blit(text, (x, y))
    return text

# colors -------------------------- #

WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
RED = (255,0,0)
YELLOW = (255,255,0)


