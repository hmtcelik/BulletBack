import pygame, sys, random, time
from data.classes import Bullet, Enemy, Player, Knife

pygame.init()

WIN_HEGIHT = 720
WIN_WIDTH = 1280
win = pygame.display.set_mode((WIN_WIDTH,WIN_HEGIHT))

pygame.display.set_caption("BulletBack (1.0)")

#importing images
walkRight = [pygame.image.load('./data/assets/R1.png'), pygame.image.load('./data/assets/R2.png'), pygame.image.load('./data/assets/R3.png'), pygame.image.load('./data/assets/R4.png'), pygame.image.load('./data/assets/R5.png'), pygame.image.load('./data/assets/R6.png'), pygame.image.load('./data/assets/R7.png'), pygame.image.load('./data/assets/R8.png')]
walkLeft = [pygame.image.load('./data/assets/L1.png'), pygame.image.load('./data/assets/L2.png'), pygame.image.load('./data/assets/L3.png'), pygame.image.load('./data/assets/L4.png'), pygame.image.load('./data/assets/L5.png'), pygame.image.load('./data/assets/L6.png'), pygame.image.load('./data/assets/L7.png'), pygame.image.load('./data/assets/L8.png')]
idleRight = [pygame.image.load('./data/assets/RIdle1.png'),pygame.image.load('./data/assets/RIdle2.png'),pygame.image.load('./data/assets/RIdle3.png'),pygame.image.load('./data/assets/RIdle4.png'),pygame.image.load('./data/assets/RIdle5.png'),pygame.image.load('./data/assets/RIdle5.png'),pygame.image.load('./data/assets/RIdle7.png'),pygame.image.load('./data/assets/RIdle8.png'),]
idleLeft = [pygame.image.load('./data/assets/LIdle1.png'),pygame.image.load('./data/assets/LIdle2.png'),pygame.image.load('./data/assets/LIdle3.png'),pygame.image.load('./data/assets/LIdle4.png'),pygame.image.load('./data/assets/LIdle5.png'),pygame.image.load('./data/assets/LIdle6.png'),pygame.image.load('./data/assets/LIdle7.png'),pygame.image.load('./data/assets/LIdle8.png'),]
bg_image = pygame.image.load('./data/assets/bg.jpg')
hero_image = pygame.image.load('./data/assets/Mid.png')
knife_img = pygame.image.load('./data/assets/knife.png')

#enemy movement
enemy_walkLeft = [pygame.image.load('./data/assets/enemy/L1E.png'),pygame.image.load('./data/assets/enemy/L2E.png'),pygame.image.load('./data/assets/enemy/L3E.png'),pygame.image.load('./data/assets/enemy/L4E.png'),pygame.image.load('./data/assets/enemy/L5E.png'),pygame.image.load('./data/assets/enemy/L6E.png'),pygame.image.load('./data/assets/enemy/L7E.png'),pygame.image.load('./data/assets/enemy/L8E.png'),]
enemy_walkRight = [pygame.image.load('./data/assets/enemy/R1E.png'),pygame.image.load('./data/assets/enemy/R2E.png'),pygame.image.load('./data/assets/enemy/R3E.png'),pygame.image.load('./data/assets/enemy/R4E.png'),pygame.image.load('./data/assets/enemy/R5E.png'),pygame.image.load('./data/assets/enemy/R6E.png'),pygame.image.load('./data/assets/enemy/R7E.png'),pygame.image.load('./data/assets/enemy/R8E.png'),]

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

#importing sfx and soundtracks
'''
#music
music_file = './sfx/test.mp3'
pygame.mixer.init()
pygame.mixer.music.load(music_file)
pygame.mixer.music.play(-1) # -1 mean loop indefinetly
'''
shootsfx = pygame.mixer.Sound('./data/sfx/shoot.wav')
hitsfx = pygame.mixer.Sound('./data/sfx/hit.wav')
deadsfx = pygame.mixer.Sound('./data/sfx/dead.wav')

#score
score = 0

#restart the game
def player_dead():
    global win, score, game_timer, enemy_creation_time, create_reset_time, right_or_left, high_score
    hero.x = WIN_WIDTH/2 - hero.width /2
    hero.y = 500
    hero.walkCt = 0
    score_font = pygame.font.Font(None, 80) 
    score_text_on_restart = score_font.render("Your Score: " + str(score), True, (0,0,0))
    win.blit(score_text_on_restart, ((WIN_WIDTH /2)-(score_text_on_restart.get_width()/2), 200 )) #(x,y) 
    i = 0
    enemies.clear()
    bullets.clear()
    knife.y = 0
    game_timer = 0
    enemy_creation_time = 0
    create_reset_time = 100
    right_or_left = 0
    hero.reloading = 0
    hero.reloading_visible = False
    #check highscore
    if not high_score > score:
        high_score = score
    while True: #changing color press R text 
        if i > 0 and i < 200:
            restart_font = pygame.font.Font(None, 40)
            restart_text = restart_font.render("Press 'R' to restart", True, (0,0,0))
            win.blit(restart_text, ((WIN_WIDTH /2)-(restart_text.get_width()/2), 270 )) #(x,y)
        else:
            restart_font = pygame.font.Font(None, 40)
            restart_text = restart_font.render("Press 'R' to restart", True, (255,255,255))
            win.blit(restart_text, ((WIN_WIDTH /2)-(restart_text.get_width()/2), 270 )) #(x,y)
            
        i += 1
        if i == 400: # changing white and black on PRESS R text
            i = 0 
        pygame.display.update()
        score = 0
        
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                    
        keys1 = pygame.key.get_pressed()
        if keys1[pygame.K_r]:
            break

#DRAW FUNCTIONS
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
    if hero.reloading_visible:
        pygame.draw.rect(win, (0, 255, 0), (hero.hitbox[0], hero.hitbox[1]-20, 50, 10), 10)
        pygame.draw.rect(win, (0, 150, 0), (hero.hitbox[0], hero.hitbox[1]-20, hero.reloading, 10), 10)

#drawing enemy movements
def enemy_draw():
    global win
    for enemy in enemies:
        if enemy.walkCt +1 >= 64:
            enemy.walkCt = 0
        
        if enemy.direction == 0:
            win.blit(enemy_walkLeft[enemy.walkCt//8], (enemy.x, enemy.y))
            enemy.walkCt += 1
        elif enemy.direction == 1:
            win.blit(enemy_walkRight[enemy.walkCt//8], (enemy.x, enemy.y))
            enemy.walkCt += 1
        
        enemy.hitbox = (enemy.x + 55, enemy.y, 40, 120)

        
        
#knife draw wich of on air
def knife_draw():
    global win
    win.blit(knife_img, (knife.x, knife.y))
    
    knife.hitbox = (knife.x + 12, knife.y + 5, 20, 32)
    

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
    score_font = pygame.font.Font(None, 35)
    score_text = score_font.render("Score: "+ str(score), True, (0,0,0))
    win.blit(score_text,(10,45))
    high_score_font = pygame.font.Font(None, 35)
    high_score_text = high_score_font.render("High Score: "+ str(high_score), True, (0,0,0)) 
    win.blit(high_score_text, (10,10))
    
    pygame.display.update()

#first knife
random_x = random.randint(0,WIN_WIDTH)
knife = Knife(random_x, 0, 10, 32)

#game loop
game_timer = 0
enemy_creation_time = 0
create_reset_time = 100
right_or_left = 0
hero = Player(WIN_WIDTH/2 - 64, 500, 128, 128)
enemies = []
bullets = []
game = True
high_score = 0
while game:
    clock.tick(64) # frame (mean: how many images use per second)
    game_timer += 1
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

    enemy_creation_time += 1
    if enemy_creation_time == create_reset_time:
        enemy_creation_time = 0
    
    if game_timer == 500:
        create_reset_time = 50
    if game_timer == 1000:
        create_reset_time = 30
    if game_timer == 2000:
        create_reset_time = 15

    #create enemy
    right_or_left = random.randint(0,1)
    if right_or_left: #this is right side (right_or_left == 1)
        if enemy_creation_time == 10:
            enemies.append(Enemy(WIN_WIDTH, 500, 128, 128, 0))
    else: #this is left side (right_or_left ==0 )
        if enemy_creation_time == 10:
            enemies.append(Enemy(0, 500, 128, 128, 1))

    #shoot timer (just blocking spamming shoot)
    if hero.reloading > 0:
        hero.reloading +=1
    if hero.reloading > 50:
        hero.reloading_visible = False
        hero.reloading = 0
                
    #bullet movement
    for bullet in bullets:
        for enemy in enemies:
            if bullet.y - bullet.radius < enemy.hitbox[1] + enemy.hitbox[3] and bullet.y + bullet.radius > enemy.hitbox[1]:
                if bullet.x + bullet.radius > enemy.hitbox[0] and bullet.x - bullet.radius < enemy.hitbox[0] + enemy.hitbox[2]:
                    hitsfx.play()
                    enemies.pop(enemies.index(enemy))
                    score += 1
                    bullets.pop(bullets.index(bullet))
                
        if bullet.x < WIN_WIDTH and bullet.x > 0:
            bullet.x += bullet.velocity * bullet.direction
        else:
            bullets.pop(bullets.index(bullet))

    keys = pygame.key.get_pressed()

    if keys[pygame.K_q] and hero.reloading == 0:          
        shootsfx.play()
        if hero.lastKey == "right":
            direction = 1
        else:
            direction = -1
        if len(bullets) < 3:
            bullets.append(Bullet(round(hero.x + hero.width // 2), round(hero.y + hero.height // 2), 6, (0,0,0), direction))
        
        hero.reloading_visible = True  
        hero.reloading = 1
        
    
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
            
    #droping knife on air
    if knife.y > 570:  
        random_x = random.randint(0,WIN_WIDTH)
        knife = Knife(random_x, 0, 10, 32)
    
    #moving knife if isnt hitted to player
    if not knife.hitted:
        knife.y += knife.velocity
    else:
        random_x = random.randint(0,WIN_WIDTH)
        knife = Knife(random_x, 0, 10, 32)
        
    #knife hit player
    if hero.hitbox[1] < knife.hitbox[1] + knife.hitbox[3]:
        if hero.hitbox[0] < knife.hitbox[0] + knife.hitbox[2] and hero.hitbox[0] + hero.hitbox[2] > knife.hitbox[0]:
            knife.hitted = True
            player_dead()    
    
    #enemy hit player
    for enemy in enemies:
        if hero.hitbox[0] + hero.hitbox[2] > enemy.hitbox[0] and hero.hitbox[0] < enemy.hitbox[0] + enemy.hitbox[2]:
            player_dead()
        

    for enemy in enemies:
        if enemy.direction == 0:
            enemy.x -= enemy.velocity
        else:
            enemy.x += enemy.velocity


    re_drawGameWindow()    
    
pygame.quit()
sys.exit()