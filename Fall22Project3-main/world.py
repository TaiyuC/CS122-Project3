from ROOM16 import Room
from monster import Monster
from monster import Super_Monster
import random
import names

class World:
    def __init__(self, gridsize = 4): # default is 4*4 world
        self.gridsize = gridsize
        self.map = [[Room() for _ in range(gridsize)]for _ in range(gridsize)]
        self.map[0][0] = Room("home", "town")
        self.map[gridsize - 1][gridsize - 1] = Room("boss","palace")
    
    def view(self): # if one find map, one can go backwards, and can use view feature. 
        for i in range(self.gridsize):
            print(self.map[i])
    
    def monster_loc(self):
        random_loc = [random.randint(1,4), random.randint(1,4)]
        while random_loc == [0,0] or random_loc == [self.gridsize - 1, self.gridsize -1]:
            random_loc = [random.randint(1,4), random.randint(1,4)]
        return random_loc
    
    def out_of_world_monster(self, loc):
        [loc1,loc2] = loc
        if 0 <= loc1 < self.gridsize:
            if 0 <= loc2 < self.gridsize:
                if loc != [1,1] or loc != [self.gridsize - 1, self.gridsize - 1]:
                    return True
        return False

    def random_neighbor(self, loc):
        [loc1,loc2] = loc
        ret_list = [] # have every possible neibor's location returned. It is garenteed to have one because how we constructed the world
        for i in range(-1,2,2): # i takes -1 or 1
            for j in range(-1,2,2): # j takes -1 or 1
                if self.out_of_world_monster([loc1+i, loc2+j]): # four cases, up/down/left/right
                    ret_list.append([loc1+i, loc2+j]) # if satisfied(in our world and is not town or palace)
        return random.choice(ret_list)
    
    def out_of_world_player(self, loc):
        [loc1,loc2] = loc
        if 0 <= loc1 < self.gridsize:
            if 0 <= loc2 < self.gridsize:
                return True
        return False

    def generate_monsters(self, n = None):
        num_monster = n if n is not None else self.gridsize
        for _ in range(num_monster):
            [loc1,loc2] = self.monster_loc()
            mon_name = "Monster " + names.get_first_name()
            if random.random() < 0.9:
                Monster(name = mon_name, loc = [loc1, loc2], world = self)
            else:
                Super_Monster(name = mon_name, loc = [loc1, loc2], world = self)
        Super_Monster(name = "You Know Who", loc = [self.gridsize-1, self.gridsize-1], world = self, hp = 200, attack = 10, defense = 20) # create boss at palace
    
    def w_has_monster(self, loc):
        loc1, loc2 = loc
        return self.map[loc1][loc2].has_monsters()
    
    def view_monster(self):
        ret_dict = {}
        ret_list = []
        for i in range(0, self.gridsize):
            for j in range(0, self.gridsize):
                the_room = self.map[i][j]
                if the_room.has_monsters():
                    for mon in the_room.monsters:
                        if str(the_room.types) in ret_dict:
                            ret_dict[str(the_room.types)] += 1
                        else: 
                            ret_dict[str(the_room.types)] = 1
                        ret_list.append(str(mon))
        return ret_dict, ret_list