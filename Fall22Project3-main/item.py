import os

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Item:
    def __init__(self, name, desc, world,):
        self.name = name
        self.desc = desc
        self.world = world
        self.loc1 = None
        self.loc2 = None
        self.hold = False

    def describe(self):
        clear()
        print(self.desc)
        print()
        input("Press enter to continue...")

    def put_in_loc(self, loc):
        self.loc1,self.loc2 = loc
        the_room = self.world.map[self.loc1][self.loc2]
        the_room.add_item(self)
