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

class player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 5
        self.left = False
        self.right = False
        self.walkCt = 0
        self.isAir = False
        self.airCount = 10

def re_drawGameWindow():        
    win.blit(bg_image, (0,0))

    if hero.walkCt +1 >= 27: # because we have 9 spirite images each movement and want to use each image on 3 frame (9*3=27)
        hero.walkCt = 0
    
    if hero.left:
        win.blit(walkLeft[hero.walkCt//3], (hero.x,hero.y)) # we divide by 3 because wanting use each png 3 frame (0/3 = 0, 1/3 = 0, 2/3 = 0, 3/3 = 1, ...)
        hero.walkCt += 1
    elif hero.right:
        win.blit(walkRight[hero.walkCt//3], (hero.x,hero.y)) # we divide by 3 because wanting use each png 3 frame (0/3 = 0, 1/3 = 0, 2/3 = 0, 3/3 = 1, ...)
        hero.walkCt += 1
    else:
        win.blit(hero_image, (hero.x,hero.y))
    
    #scoreboard
    font = pygame.font.Font('freesansbold.ttf', 24)
    score_text = font.render("Score: 0",True,(0,0,0))
    win.blit(score_text,(10,10))
    
    pygame.display.update()
    
#game loop
hero = player(50, 430, 64, 64)
game = True
while game:
    clock.tick(27) # frame (mean: how many images use per second)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and hero.x > 0:
        hero.x -= hero.velocity     # the top and left coordinate is (0,0), if going right; x increase, if going bottom y increase
        hero.left = True
        hero.right = False
    elif keys[pygame.K_RIGHT] and hero.x < WIN_WIDTH - hero.width: 
        hero.x += hero.velocity
        hero.right = True
        hero.left = False
    else:
        hero.left = False
        hero.right = False
        hero.walkCt = 0
    
    if keys[pygame.K_w]:
        hero.y -= hero.velocity
    if not hero.isAir:
        if keys[pygame.K_UP] and hero.y > 0:
            hero.isAir = True
            hero.left = False
            hero.right = False
            hero.walkCt = 0
    elif hero.isAir:
        if hero.airCount >= -10: 
            hero.y -= (hero.airCount * 3)
            hero.airCount -= 1
        else:
            hero.isAir = False
            hero.airCount = 10

    re_drawGameWindow()
    
    
pygame.quit()