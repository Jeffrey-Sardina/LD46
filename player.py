class Player:
    def __init__(self):
        self.hp = 10
        self.max_hp = 10
    
    def damage(self, value):
        self.hp -= value

    def heal(self, value):
        self.hp += value
