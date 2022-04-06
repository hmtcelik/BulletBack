from tkinter.tix import Tree
from numpy import False_
import pygame, sys, random, time
from actors import Bullet, Enemy, Player, Knife

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
knife_img = pygame.image.load('./assets/knife.png')

#enemy movement
enemy_walkLeft = [pygame.image.load('./assets/enemy/L1E.png'),pygame.image.load('./assets/enemy/L2E.png'),pygame.image.load('./assets/enemy/L3E.png'),pygame.image.load('./assets/enemy/L4E.png'),pygame.image.load('./assets/enemy/L5E.png'),pygame.image.load('./assets/enemy/L6E.png'),pygame.image.load('./assets/enemy/L7E.png'),pygame.image.load('./assets/enemy/L8E.png'),]
enemy_walkRight = [pygame.image.load('./assets/enemy/R1E.png'),pygame.image.load('./assets/enemy/R2E.png'),pygame.image.load('./assets/enemy/R3E.png'),pygame.image.load('./assets/enemy/R4E.png'),pygame.image.load('./assets/enemy/R5E.png'),pygame.image.load('./assets/enemy/R6E.png'),pygame.image.load('./assets/enemy/R7E.png'),pygame.image.load('./assets/enemy/R8E.png'),]

clock = pygame.time.Clock()

a=0
#transform images
for i in range(8):
    walkRight[a] = pygame.transform.scale(walkRight[a], (128,128))
    walkLeft[a] = pygame.transform.scale(walkLeft[a], (128,128))
    idleRight[a] = pygame.transform.scale(idleRight[a], (128,128))
    idleLeft[a] = pygame.transform.scale(idleLeft[a], (128,128))
    a += 1

a=0
for i in range(8):
    enemy_walkLeft[a] = pygame.transform.scale(enemy_walkLeft[a], (128,128)) 
    enemy_walkRight[a] = pygame.transform.scale(enemy_walkRight[a], (128,128)) 
    a += 1

hero_image = pygame.transform.scale(hero_image, (128,128))

knife_img = pygame.transform.rotate(knife_img, 45)

#drawing hero movements
def hero_draw():
    global win
    if hero.walkCt +1 >= 64: # because we have 8 spirite images each movement and want to use each image on 8 frame (8*8=64)
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
    
    hero.hitbox = (hero.x + 35, hero.y, 56, 120)
    pygame.draw.rect(win, (255, 0, 0), (hero.hitbox), 2)

#drawing enemy movements
def enemy_draw():
    global win
    if enemy.walkCt +1 >= 64:
        enemy.walkCt = 0
    
    if enemy.left:
        win.blit(enemy_walkLeft[enemy.walkCt//8], (enemy.x, enemy.y))
        enemy.walkCt += 1
    elif enemy.right:
        win.blit(enemy_walkRight[enemy.walkCt//8], (enemy.x, enemy.y))
        enemy.walkCt += 1
    
    enemy.hitbox = (enemy.x + 45, enemy.y, 52, 120)
    pygame.draw.rect(win, (255, 0, 0), (enemy.hitbox), 2)
        
#knife draw wich of on air
def knife_draw():
    global win
    win.blit(knife_img, (knife.x, knife.y))
    
    knife.hitbox = (knife.x + 12, knife.y + 5, 20, 32)
    pygame.draw.rect(win, (255, 0, 0), (knife.hitbox), 2)

#draw bullet
def draw_bullet():
    global win
    for bullet in bullets:
        pygame.draw.circle(win, bullet.color, (bullet.x, bullet.y), bullet.radius)    

#main draw func
def re_drawGameWindow():        
    win.blit(bg_image, (0,0))
    hero_draw()
    enemy_draw()
    knife_draw() 
    draw_bullet()
    
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
enemy = Enemy(600, 500, 128,128)
bullets = []
shootCt = 0
game = True
while game:
    clock.tick(64) # frame (mean: how many images use per second)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    #shoot timer (just blocking spamming shoot)
    if shootCt > 0:
        shootCt +=1
    if shootCt > 60:
        shootCt = 0
        
    #bullet movement
    for bullet in bullets:
        if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
            if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                enemy.hit()
                bullets.pop(bullets.index(bullet))
                
        
        if bullet.x < WIN_WIDTH and bullet.x > 0:
            bullet.x += bullet.velocity * bullet.direction
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q] and shootCt == 0:          
        if hero.lastKey == "right":
            direction = 1
        else:
            direction = -1
        if len(bullets) < 3:
            bullets.append(Bullet(round(hero.x + hero.width // 2), round(hero.y + hero.height // 2), 6, (0,0,0), direction))
          
        shootCt = 1
    
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
        
    if not hero.isAir:
        if keys[pygame.K_UP] and hero.y > 0:
            hero.isAir = True
            hero.left = False
            hero.right = False
            hero.walkCt = 0
    elif hero.isAir:
        if hero.airCount >= -10:
            if hero.airCount > 0:
                negative = 1
            else:
                negative = -1
            hero.y -= (hero.airCount ** 2) / 2 * negative  # momentum of jump
            hero.airCount -= 1
        else:
            hero.isAir = False
            hero.airCount = 10
            
    #droping knife on air
    if knife.y > 570:  
        random_x = random.randint(0,WIN_WIDTH)
        knife = Knife(random_x, 0, 10, 32)
    knife.y += knife.velocity #moving knife
    
    #dying

        
    if enemy.x >= 800:
        enemy.left = True
        enemy.right = False
    if enemy.x <= 300:
        enemy.right = True
        enemy.left = False

    if enemy.left:
        enemy.x -= enemy.velocity
    else:
        enemy.x += enemy.velocity


    re_drawGameWindow()    
    
pygame.quit()
sys.exit()