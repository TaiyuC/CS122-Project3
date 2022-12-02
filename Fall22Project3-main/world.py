from ROOM16 import Room
from monster import Monster
from monster import Super_Monster
from item import Item
import random
import names

class World:
    def __init__(self, gridsize = 4): # default is 4*4 world
        """create a world with adjustable size. It stores room's information by list."""
        self.gridsize = gridsize
        self.map = [[Room() for _ in range(gridsize)]for _ in range(gridsize)] 
        self.map[0][0] = Room("home", "town") # player start at town
        self.map[gridsize - 1][gridsize - 1] = Room("boss","palace") # boss is the farest from the player
    
    def view(self): # TODO if one find map, one can go backwards, and can use view feature. 
        for i in range(self.gridsize):
            print(self.map[i])
    
    def monster_loc(self):
        """random get a location that is neither town or palace. That is to say the monster can only born and move in other places"""
        random_loc = [random.randint(1,4), random.randint(1,4)]
        while random_loc == [0,0] or random_loc == [self.gridsize - 1, self.gridsize -1]:
            random_loc = [random.randint(1,4), random.randint(1,4)]
        return random_loc
    
    def out_of_world_monster(self, loc):
        """input a location and returns True if it is in the world and not palace or town. Else false."""
        [loc1,loc2] = loc
        if 0 <= loc1 < self.gridsize:
            if 0 <= loc2 < self.gridsize:
                if loc != [1,1] or loc != [self.gridsize - 1, self.gridsize - 1]:
                    return True
        return False

    def random_neighbor(self, loc):
        """check every possible location the monster can move to."""
        [loc1,loc2] = loc
        ret_list = [] # have every possible neibor's location returned. It is garenteed to have one because how we constructed the world
        for i in range(-1,2,2): # i takes -1 or 1
            for j in range(-1,2,2): # j takes -1 or 1
                if self.out_of_world_monster([loc1+i, loc2+j]): # four cases, up/down/left/right
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
            mon_name = "Monster " + names.get_first_name()
            if random.random() < 0.9: # randomly have normal monster and super monster, super monster is stronger.
                Monster(name = mon_name, loc = [loc1, loc2], world = self)
            else:
                Super_Monster(name = mon_name, loc = [loc1, loc2], world = self) # we have the super monster which is harder to battle
        Super_Monster(name = "You Know Who", loc = [self.gridsize-1, self.gridsize-1], world = self, hp = 200, attack = 10, defense = 20) # create boss at palace
    
    def w_has_monster(self, loc):
        """determine whether this location in the world has monster"""
        loc1, loc2 = loc
        return self.map[loc1][loc2].has_monsters()
    
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

    def initialize_item(self):
        """put wood in forest, put acient gear in dessert, put magnetic in montain"""
        dessert_loc = []
        for i in range(0, self.gridsize):
            for j in range(0, self.gridsize):
                if self.map[i][j].types == "forest":
                    item = Item(name = "wood", desc = "we may use wood to make something", world = self)
                    item.put_in_loc([i,j])
                elif self.map[i][j].types == "dessert":
                    item = Item(name = "acient gear", desc = "we may use acient gear to make something", world = self)
                    item.put_in_loc([i,j])
                    dessert_loc.append( [i,j] )
                elif self.map[i][j].types == "montain":
                    item = Item(name = "magnetic", desc = "we may use magnetic to make something", world = self)
                    item.put_in_loc([i,j])
        if len(dessert_loc) > 0:
            the_loc = random.choice(dessert_loc)
            core = Item(name = "acient core", desc = "we may use acient core make something great", world = self)
            core.put_in_loc(the_loc)
