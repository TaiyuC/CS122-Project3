import random

class Room:
    def __init__(self, description = "random room", types = None):
        self.desc = description # description of the room, which is not quiet used in the game
        self.monsters = [] # monsters in the room as list
#        self.exits = [False, False, False, False] #This locked door function is not what I wanted
        self.items = [] # items in the room
        self.rep_type = random.choice(["forest_", "desert_", "montain"]) if types == None else types # 5 types of room: forest, desert, montain, town(hp recover, no monster), palace(boss). 
        self.types = self.rep_type.replace("_","",-1) # To make the "map" looks like a sqaure, I put some "_", this is just get rid of that.

    def __repr__(self):
        return self.rep_type # used on map

    def add_item(self, item): # just add or delete item
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)

    def add_monster(self, monster): # add or delete monster
        self.monsters.append(monster)
    def remove_monster(self, monster):
        self.monsters.remove(monster)

    def has_items(self): # whether having item/monster
        return self.items != []
    def has_monsters(self):
        return self.monsters != []

    def get_monster_by_name(self, name): # get the monster by its either name or shortname
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
            elif i.short_name.lower() == name.lower():
                return i
        return False
    
    def get_item_by_name(self, name): # get the name of an item
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    
    # def emergency_exit(self):
    #     return random.choice(self.exits)
    
    #def get_destination(self):
