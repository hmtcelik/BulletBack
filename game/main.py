import pygame, sys, random
from actors import Player, Knife

pygame.init()

WIN_HEGIHT = 720
WIN_WIDTH = 1280
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEGIHT))

pygame.display.set_caption("Airblade")

#importing images
walkRight = [pygame.image.load('./assets/R1.png'), pygame.image.load('./assets/R2.png'), pygame.image.load('./assets/R3.png'), pygame.image.load('./assets/R4.png'), pygame.image.load('./assets/R5.png'), pygame.image.load('./assets/R6.png'), pygame.image.load('./assets/R7.png'), pygame.image.load('./assets/R8.png')]
walkLeft = [pygame.image.load('./assets/L1.png'), pygame.image.load('./assets/L2.png'), pygame.image.load('./assets/L3.png'), pygame.image.load('./assets/L4.png'), pygame.image.load('./assets/L5.png'), pygame.image.load('./assets/L6.png'), pygame.image.load('./assets/L7.png'), pygame.image.load('./assets/L8.png')]
idleRight = [pygame.image.load('./assets/RIdle1.png'),pygame.image.load('./assets/RIdle2.png'),pygame.image.load('./assets/RIdle3.png'),pygame.image.load('./assets/RIdle4.png'),pygame.image.load('./assets/RIdle5.png'),pygame.image.load('./assets/RIdle5.png'),pygame.image.load('./assets/RIdle7.png'),pygame.image.load('./assets/RIdle8.png'),]
idleLeft = [pygame.image.load('./assets/LIdle1.png'),pygame.image.load('./assets/LIdle2.png'),pygame.image.load('./assets/LIdle3.png'),pygame.image.load('./assets/LIdle4.png'),pygame.image.load('./assets/LIdle5.png'),pygame.image.load('./assets/LIdle6.png'),pygame.image.load('./assets/LIdle7.png'),pygame.image.load('./assets/LIdle8.png'),]
bg_image = pygame.image.load('./assets/bg.jpg')
hero_image = pygame.image.load('./assets/Mid.png')

clock = pygame.time.Clock()

a=0
#transform images
for i in range(8):
    walkRight[a] = pygame.transform.scale(walkRight[a], (128,128))
    walkLeft[a] = pygame.transform.scale(walkLeft[a], (128,128))
    idleRight[a] = pygame.transform.scale(idleRight[a], (128,128))
    idleLeft[a] = pygame.transform.scale(idleLeft[a], (128,128))
    a += 1

hero_image = pygame.transform.scale(hero_image, (128,128))

def re_drawGameWindow():        
    win.blit(bg_image, (0,0))

    #walking hero
    if hero.walkCt +1 >= 64: # because we have 9 spirite images each movement and want to use each image on 3 frame (9*3=27)
        hero.walkCt = 0
    if hero.idleCt +1 >= 64:
        hero.idleCt = 0
    
    if hero.left:
        win.blit(walkLeft[hero.walkCt//8], (hero.x,hero.y)) # we divide by 3 because wanting use each png 3 frame (0/3 = 0, 1/3 = 0, 2/3 = 0, 3/3 = 1, ...)
        hero.walkCt += 1
    elif hero.right:
        win.blit(walkRight[hero.walkCt//8], (hero.x,hero.y)) # we divide by 3 because wanting use each png 3 frame (0/3 = 0, 1/3 = 0, 2/3 = 0, 3/3 = 1, ...)
        hero.walkCt += 1
    else:
        if hero.lastKey == "right":    
            win.blit(idleRight[hero.idleCt//8], (hero.x, hero.y))
            hero.idleCt += 1
        else:
            win.blit(idleLeft[hero.idleCt//8], (hero.x, hero.y))
            hero.idleCt += 1
    
    #knife on air
    pygame.draw.rect(win, knife.color, (knife.x, knife.y, knife.width, knife.height))
    
    #scoreboard
    font = pygame.font.Font('freesansbold.ttf', 24)
    score_text = font.render("Score: 0",True,(0,0,0))
    win.blit(score_text,(10,10))
    
    pygame.display.update()
    
#music
'''
music_file = './sfx/test.mp3'
pygame.mixer.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1) # -1 mean loop indefinetly
''' 

#first knife
random_x = random.randint(0,WIN_WIDTH)
knife = Knife(random_x, 0, 10, 32)

#game loop
hero = Player(50, 500, 128, 128)
game = True
while game:
    clock.tick(64) # frame (mean: how many images use per second)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and hero.x > 0:
        hero.x -= hero.velocity     # the top and left coordinate is (0,0), if going right; x increase, if going bottom y increase
        hero.left = True
        hero.right = False
        hero.lastKey = "left"
    elif keys[pygame.K_RIGHT] and hero.x < WIN_WIDTH - hero.width: 
        hero.x += hero.velocity
        hero.right = True
        hero.left = False
        hero.lastKey = "right"
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
            
    #droping knife on air
    if knife.y > WIN_HEGIHT:  
        random_x = random.randint(0,WIN_WIDTH)
        knife = Knife(random_x, 0, 10, 32)
    knife.y += knife.velocity #moving knife

    re_drawGameWindow()    
    
pygame.quit()
sys.exit()