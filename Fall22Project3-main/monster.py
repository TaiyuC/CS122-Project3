import random
import updater

class Monster:
    def __init__(self, name, loc, world, hp = None, attack = None, defense = None, short_name = None):
        self.name = name
        self.hp = random.randint(10,20) if hp == None else hp # randomly have hp, attack, defense, 
        #self.maxhp = int(self.hp)
        self.attack = random.randint(1,8) if attack == None else attack
        self.defense = random.randint(1,8) if defense == None else defense
        self.world = world # use this world system we can have world registered here
        [self.loc1, self.loc2] = loc
        self.world.map[self.loc1][self.loc2].add_monster(self)
        self.short_name = short_name
        #self.captured = True
        updater.register(self)

    def __repr__(self):
        str = f" {self.name}: {self.hp} HP {self.attack} ATK {self.defense} DEF"
        return str
    
    def glimpse(self):
        str = f" {self.name}: {self.hp} HP "
        return str

    def update(self):
        if random.random() < .1:
            self.move_to(self.world.random_neighbor([self.loc1, self.loc2]))
        
    def move_to(self, loc):
        [loc1,loc2] = loc
        self.world.map[self.loc1][self.loc2].remove_monster(self)
        self.loc1 = loc1
        self.loc2 = loc2
        print(loc1)
        print(loc2)
        self.world.map[loc1][loc2].add_monster(self)

    def die(self):
        self.world.map[self.loc1][self.loc2].remove_monster(self)
        updater.deregister(self)

class Super_Monster(Monster): # the difference is super monster is not going to move.
    def __init__(self, name, loc, world, hp = None, attack = None, defense = None, short_name= None):
        self.name = name if name == "TaoTie" else ("Fierce" + name)
        self.hp = random.randint(20,30) if hp == None else hp # randomly have hp, attack, defense, 
        #self.maxhp = int(self.hp)
        self.attack = random.randint(7,10) if attack == None else attack
        self.defense = random.randint(7,10) if defense == None else defense
        self.world = world # use this world system we can have world registered here
        [self.loc1, self.loc2] = loc
        self.world.map[self.loc1][self.loc2].add_monster(self)
        self.short_name = "F" + short_name
        #self.captured = False
    
    def die(self):
        self.world.map[self.loc1][self.loc2].remove_monster(self)
    
    def __repr__(self):
        str = f" {self.name} about {self.hp + random.randint(-int(self.hp/5), int(self.hp/5))} HP"
        return str
    
    def glimpse(self):
        str = f" {self.name}: X HP "
        return str
    