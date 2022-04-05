from turtle import right


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
        
class Knife(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.velocity = 7
        self.color = (0,0,0)
