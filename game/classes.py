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
    def __init__(self, x, y, width, height, direction):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 3
        self.walkCt = 0
        self.direction = direction
        self.hitbox = (self.x + 35, self.y, 35, 120)

class Bullet(object):
    def __init__(self, x, y, radius, color, direction):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.direction = direction
        self.velocity = 10