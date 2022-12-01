import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, world, hp = 50):
        self.loc1 = 0 # start in town
        self.loc2 = 0
        self.items = [] 
        self.hp = hp
        self.maxhp = int(self.hp)
        self.attack = 10
        self.defense = 10
        self.monster = []
        self.alive = True
        self.map = False
        self.world = world

    def __repr__(self):
        return f"you are in {self.world.map[self.loc1][self.loc2]}"
    
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, direction):
        if direction == "up":
            whether = self.world.out_of_world_player([self.loc1 - 1,self.loc2])
            if whether:
                self.loc1 -= 1
                return True
        elif direction == "down":
            whether = self.world.out_of_world_player([self.loc1 + 1,self.loc2])
            if whether:
                self.loc1 += 1
                return True
        elif direction == "left":
            whether = self.world.out_of_world_player([self.loc1,self.loc2 - 1])
            if whether:
                self.loc2 -= 1
                return True
        elif direction == "right":
            whether = self.world.out_of_world_player([self.loc1,self.loc2 + 1])
            if whether:
                self.loc2 += 1
                return True
        else:
            return False

    def check_direction(self, direction):
        if direction == "up":
            return self.world.out_of_world_player([self.loc1 - 1,self.loc2])
        elif direction == "down":
            return self.world.out_of_world_player([self.loc1 + 1,self.loc2])
        elif direction == "left":
            return self.world.out_of_world_player([self.loc1,self.loc2 - 1])
        elif direction == "right":
            return self.world.out_of_world_player([self.loc1,self.loc2 + 1])
        else:
            return False


    # def pickup(self, item):
    #     self.items.append(item)
    #     item.loc = self
    #     self.location.remove_item(item)

    # def show_inventory(self):
    #     clear()
    #     print("You are currently carrying:")
    #     print()
    #     for i in self.items:
    #         print(i.name)
    #     print()
    #     input("Press enter to continue...")

    def attack_monster(self, mon):
        clear()
        print(f"You are attacking {mon.name}: hp {mon.hp}, attack {mon.attack}, defense{mon.defense} ")
        print()
        print("Your health is " + str(self.hp) + ".")
        print()
        while self.alive:
            self.hp -= int(5 ** (mon.attack/self.defense))
            mon.hp -= int(5 ** (mon.attack/self.defense))
            if mon.hp < 0:
                mon.die()
                print("You win. Your health is now " + str(self.hp) + ".")
                break
            elif self.hp < self.maxhp/3:
                print("You are badly injured. Your health is now " + str(self.hp) + ".")
            if self.hp < 0:
                print("You lose.")
                self.alive = False
        print()
        input("Press enter to continue...")
