import pygame

pygame.init()

WIN_HEGIHT = 500
WIN_WIDTH = 500
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEGIHT))

pygame.display.set_caption("Airblade")

#character
x = 0
y = 0
width = 40
height = 60
velocity = 10

run = True

while run:
    pygame.time.delay(100)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > 0:
        x -= velocity     # the top and left coordinate is (0,0), if going right; x increase, if going bottom y increase
    if keys[pygame.K_RIGHT] and x < WIN_WIDTH - width: 
        x += velocity
    if keys[pygame.K_UP] and y > 0:
        y -= velocity
    if keys[pygame.K_DOWN] and y < WIN_HEGIHT - height:
        y += velocity
        
    win.fill((0,0,0))
    pygame.draw.rect(win, (255, 0, 0), (x, y, width, height)) # (base surface, (color), (x position, y position, width, height)) 
    pygame.display.update()
    
    
pygame.quit()