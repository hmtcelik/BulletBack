import pygame

pygame.init()

WIN_HEGIHT = 500
WIN_WIDTH = 500
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEGIHT))

pygame.display.set_caption("Airblade")

#importing images
walkRight = [pygame.image.load('./images/R1.png'), pygame.image.load('./images/R2.png'), pygame.image.load('./images/R3.png'), pygame.image.load('./images/R4.png'), pygame.image.load('./images/R5.png'), pygame.image.load('./images/R6.png'), pygame.image.load('./images/R7.png'), pygame.image.load('./images/R8.png'), pygame.image.load('./images/R9.png')]
walkLeft = [pygame.image.load('./images/L1.png'), pygame.image.load('./images/L2.png'), pygame.image.load('./images/L3.png'), pygame.image.load('./images/L4.png'), pygame.image.load('./images/L5.png'), pygame.image.load('./images/L6.png'), pygame.image.load('./images/L7.png'), pygame.image.load('./images/L8.png'), pygame.image.load('./images/L9.png')]
bg_image = pygame.image.load('./images/bg.jpg')
hero_image = pygame.image.load('./images/Mid.png')

clock = pygame.time.Clock()

#character
width = 64
height = 64
x = 0
y = WIN_HEGIHT - height
velocity = 10
left = False
right = False
walkCt = 0

isAir = False
airCount = 10

game = True

def re_drawGameWindow():        
    global walkCt
    win.blit(bg_image, (0,0))

    if walkCt +1 >= 27: # because we have 9 spirite images each movement and want to use each image on 3 frame (9*3=27)
        walkCt = 0
    
    if left:
        win.blit(walkLeft[walkCt//3], (x,y)) # we divide by 3 because wanting use each png 3 frame (0/3 = 0, 1/3 = 0, 2/3 = 0, 3/3 = 1, ...)
        walkCt += 1
    elif right:
        win.blit(walkRight[walkCt//3], (x,y)) # we divide by 3 because wanting use each png 3 frame (0/3 = 0, 1/3 = 0, 2/3 = 0, 3/3 = 1, ...)
        walkCt += 1
    else:
        win.blit(hero_image, (x,y))

    pygame.display.update()
    
#game loop
while game:
    clock.tick(27) # frame (mean: how many images use per second)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and x > 0:
        x -= velocity     # the top and left coordinate is (0,0), if going right; x increase, if going bottom y increase
        left = True
        right = False
    elif keys[pygame.K_RIGHT] and x < WIN_WIDTH - width: 
        x += velocity
        right = True
        left = False
    else:
        left = False
        right = False
        walkCt = 0
    
    if keys[pygame.K_w]:
        y -= velocity
    if not isAir:
        if keys[pygame.K_UP] and y > 0:
            isAir = True
            left = False
            right = False
            walkCt = 0
    elif isAir:
        if airCount >= -10: 
            y -= (airCount * 3)
            airCount -= 1
        else:
            isAir = False
            airCount = 10
    
    re_drawGameWindow()
    
    
pygame.quit()