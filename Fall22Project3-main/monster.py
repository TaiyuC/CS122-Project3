import random
import updater

class Monster:
    def __init__(self, name, loc, world, hp = None, attack = None, defense = None):
        self.name = name
        self.hp = random.randint(10,20) if hp == None else hp # randomly have hp, attack, defense, 
        self.maxhp = int(self.hp)
        self.attack = random.randint(1,8) if attack == None else attack
        self.defense = random.randint(1,8) if defense == None else defense
        self.world = world # use this world system we can have world registered here
        [self.loc1, self.loc2] = loc
        self.world.map[self.loc1][self.loc2].add_monster(self)
        self.captured = True
        updater.register(self)

    def __repr__(self):
        str = f"_{self.name}_ hp:{self.hp}"
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

class Super_Monster(Monster):
    def __init__(self, name, loc, world, hp = None, attack = None, defense = None):
        self.name = name if name == "You Know Who" else "SUPER " + name
        self.hp = random.randint(20,30) if hp == None else hp # randomly have hp, attack, defense, 
        self.maxhp = int(self.hp)
        self.attack = random.randint(7,10) if attack == None else attack
        self.defense = random.randint(7,10) if defense == None else defense
        self.world = world # use this world system we can have world registered here
        [self.loc1, self.loc2] = loc
        self.world.map[self.loc1][self.loc2].add_monster(self)
        self.captured = False
        updater.register(self)

