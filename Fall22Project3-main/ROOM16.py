import random


class Room:
    def __init__(self, description = "random room", types = None):
        self.desc = description
        self.monsters = []
#        self.exits = [False, False, False, False]
        self.items = []
        self.rep_type = random.choice(["forest_", "desert_", "montain"]) if types == None else types # 5 types of room: forest, desert, montain, town(hp recover, no monster), palace(boss). 
        self.types = self.rep_type.replace("_","",-1)

    def __repr__(self):
        if "": # if high level monster in the room, give a warning/ don't know other info but higher chance to get reward
            ""
        #return f"description : {self.desc}, type : {self.types}, monster(s): {len(self.monsters)}, item(s): {len(self.items)}" 
        # only can see number of monsters and number of items.
        return self.rep_type

    def add_item(self, item):
        self.items.append(item)
    def remove_item(self, item):
        self.items.remove(item)

    def add_monster(self, monster):
        self.monsters.append(monster)
    def remove_monster(self, monster):
        self.monsters.remove(monster)

    def has_items(self):
        return self.items != []
    def has_monsters(self):
        return self.monsters != []

    def get_monster_by_name(self, name):
        for i in self.monsters:
            if i.name.lower() == name.lower():
                return i
            elif i.short_name.lower() == name.lower():
                return i
        return False
    
    def get_item_by_name(self, name):
        for i in self.items:
            if i.name.lower() == name.lower():
                return i
        return False
    
    # def emergency_exit(self):
    #     return random.choice(self.exits)
    
    #def get_destination(self):
