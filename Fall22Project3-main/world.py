from ROOM16 import Room
from monster import Monster
from monster import Super_Monster
from item import Item
import random

class World:
    def __init__(self, gridsize = 4): # default is 4*4 world
        """create a world with adjustable size. It stores room's information by list."""
        self.gridsize = gridsize
        self.map = [[Room() for _ in range(gridsize)]for _ in range(gridsize)] 
        self.map[0][0] = Room("home, always no monster", "_town__") # player start at town
        self.map[gridsize - 1][gridsize - 1] = Room("TaoTie, an acient beast, lives here.","palace_") # boss is the farest from the player
    
    def view(self): # TODO if one find map, one can go backwards, and can use view feature. 
        for i in range(self.gridsize):
            print(self.map[i])
    
    def monster_loc(self):
        """random get a location that is neither town or palace. That is to say the monster can only born and move in other places"""
        random_loc = [random.randint(0,self.gridsize-1), random.randint(0,self.gridsize-1)]
        while random_loc == [0,0] or random_loc == [self.gridsize - 1, self.gridsize -1]:
            random_loc = [random.randint(0,self.gridsize-1), random.randint(1,self.gridsize-1)]
        return random_loc
    
    def in_world_monster(self, loc):
        """input a location and returns True if it is in the world and not palace or town. Else false."""
        [loc1,loc2] = loc
        if 0 <= loc1 < self.gridsize:
            if 0 <= loc2 < self.gridsize:
                if loc != [0,0] and loc != [self.gridsize - 1, self.gridsize - 1]:
                    return True
        return False

    def random_neighbor(self, loc):
        """check every possible location the monster can move to."""
        [loc1,loc2] = loc
        ret_list = [] # have every possible neibor's location returned. It is garenteed to have one because how we constructed the world
        for i in range(-1,2,2): # i takes -1 or 1
            for j in range(-1,2,2): # j takes -1 or 1
                if self.in_world_monster([loc1+i, loc2+j]): # four cases, up/down/left/right
                    ret_list.append([loc1+i, loc2+j]) # if satisfied(in our world and is not town or palace)
        return random.choice(ret_list)
    
    def out_of_world_player(self, loc):
        """check every possible location the player can move to. the player can go to palace and town."""
        [loc1,loc2] = loc
        if 0 <= loc1 < self.gridsize:
            if 0 <= loc2 < self.gridsize:
                return True
        return False

    def generate_monsters(self, n = None):
        """generate monsters to locations that is neither town nor palace"""
        num_monster = n if n is not None else self.gridsize
        for _ in range(num_monster):
            [loc1,loc2] = self.monster_loc()
            self.create_mon(loc1, loc2)
        Super_Monster(name = "TaoTie", loc = [self.gridsize-1, self.gridsize-1], world = self, hp = 150, attack = 15, defense = 20, short_name = "TT") # create boss at palace
    
    def w_has_monster(self, loc):
        """determine whether this location in the world has monster"""
        loc1, loc2 = loc
        return self.map[loc1][loc2].has_monsters()
    
    def glimpse_monster(self):
        ret_list = []
        for i in range(0, self.gridsize):
            for j in range(0, self.gridsize):
                the_room = self.map[i][j]
                if the_room.has_monsters():
                    for mon in the_room.monsters:
                        ret_list.append(str(mon.glimpse()))
        return ret_list
        

    def view_monster(self):
        """gives player the chance to see how many monsters in each types of land (as dictionary), and see the names of monsters (as list)"""
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
    
    def item_by_roomtype(self, i, j):
        """put wood in forest, put acient gear in desert, put magnetic in montain"""
        if self.map[i][j].types == "forest":
            item = Item(name = "wood", desc = "we may use wood to make something", world = self)
            item.put_in_loc([i,j])
        elif self.map[i][j].types == "desert":
            item = Item(name = "acient gear", desc = "we may use acient gear to make something", world = self)
            item.put_in_loc([i,j])
        elif self.map[i][j].types == "montain":
            item = Item(name = "magnetic", desc = "we may use magnetic to make something", world = self)
            item.put_in_loc([i,j])
    
    def get_desert_loc(self):
            desert_loc = []
            for i in range(0, self.gridsize):
                for j in range(0, self.gridsize):
                    if self.map[i][j].types == "desert":
                        desert_loc.append( [i,j] )
            return desert_loc

    def initialize_item(self):
        for i in range(0, self.gridsize):
            for j in range(0, self.gridsize):
                self.item_by_roomtype(i, j)
        des_loc = self.get_desert_loc()
        if len(des_loc) > 0:
            the_loc = random.choice(des_loc)
            core = Item(name = "acient core", desc = "we may use acient core make something interesting", world = self)
            core.put_in_loc(the_loc)
            Super_Monster(name = "QiongQi the core guard", loc = the_loc, world = self, attack = 15, defense= 15, hp = 50, short_name="QQ")
    
    def item_new(self, n = 1):
        for _ in range(n):
            loc1, loc2 = self.monster_loc()
            self.item_by_roomtype(loc1, loc2)
    
    def create_mon(self, loc1, loc2):
        mon_name = random.choice(["NineTails", "Unicorn", "GuanShu", "Zheng", "GuDiao", "Lili", "ZhuYin", "QiongQi", "HunDun"])
        mon_short_name = ''.join([c for c in mon_name if c.isupper()])
        if mon_name != "HunDun" and mon_name != "QiongQi": # randomly have normal monster and super monster(QiongQi, ZhuYin), super monster is stronger.
            Monster(name = mon_name, loc = [loc1, loc2], world = self, short_name = mon_short_name)
        else:
            Super_Monster(name = mon_name, loc = [loc1, loc2], world = self, short_name= mon_short_name) # we have the super monster which is harder to battle

    def mon_new(self, n = 1):
        for _ in range(n):
            loc1, loc2 = self.monster_loc()
            self.create_mon(loc1, loc2)