class Player(object):
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
        self.idleCt = 0
        self.lastKey = "right"
        self.hitbox = (self.x + 35, self.y, 56, 120)
        self.reloading = 0
        self.reloading_visible = False
    
    def hit_knife(self):
        print("I am dead")
        
class Knife(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 10
        self.hitbox = (self.x + 12, self.y+5, 20, 32)
        self.hitted = False

class Enemy(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 3
        self.walkCt = 0
        self.left = True
        self.right = False
        self.hitbox = (self.x + 45, self.y, 52, 120)
    
    def hit(self):
        print("yeah")

class Bullet(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 10