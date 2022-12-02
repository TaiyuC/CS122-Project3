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
        self.world = world
        self.map = False
        self.acient_detector = False
        self.railgun = False

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
    
    def teleport(self):
        self.hp = self.maxhp
        self.loc1 = 0
        self.loc2 = 0

    def pickup(self, item):
        self.items.append(item)
        item.hold = False
        item.world.map[item.loc1][item.loc2].remove_item(item)

    def show_inventory(self):
        clear()
        print("You are currently carrying:")
        print()
        for i in self.items:
            print(i.name)
        print()
        input("Press enter to continue...")

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
                if self.hp < self.maxhp/3:
                    print("You are badly injured. Your health is now " + str(self.hp) + ".")
                else:
                    print("You win. Your health is now " + str(self.hp) + ".")
                break
            if mon.hp < mon.hp/3:
                print(f"{mon.name} is badly injured, it has {mon.hp} HP.")
            if self.hp < 0:
                print("You lose.")
                self.alive = False
        print()
        input("Press enter to continue...")
    
    def count_item(self):
        ret_dict = {}
        for i in self.items:
            the_name = i.name
            if the_name in ret_dict:
                ret_dict[the_name] += 1
            else:
                ret_dict[the_name] = 1
        return ret_dict
    
    def can_craft(self):
        dict = self.count_item()
        if "wood" in dict and "acient gear" in dict and "magnetic" in dict: # wood can be used to build 
            if dict["wood"] > 3 and dict["acient gear"] > 3 and dict["magnetic"] > 3:
                return True
        if "acient gear" in dict and "acient core" in dict:
            if dict["acient gear"] > 5:
                return True
        if "magnetic" in dict and "wood" in dict:
            if dict["magnetic"] > 5 and dict["wood"] >3:
                return True
        return False
    
    def item_remove(self, inp_name, num = 1):
        for _ in range(num):
            for i in self.items:
                if i.name == inp_name:
                    self.items.remove(i)

    def make_craft(self):
        if self.map and self.acient_detector and self.railgun:
            print("you've made everything")
            print()
            input("Press enter to continue...")
        else:
            if self.can_craft():
                clear()
                dict = self.count_item()
                can_make_list = []
                if "magnetic" in dict and "wood" in dict:
                    if dict["magnetic"] > 5 and dict["wood"] >3 and not self.map:
                        can_make_list.append("map")
                if "acient gear" in dict and "acient core" in dict:
                    if dict["acient gear"] > 5 and dict["acient core"] > 1 and not self.acient_detector:
                        can_make_list.append("acient detector")
                if "wood" in dict and "acient gear" in dict and "magnetic" in dict:
                    if dict["wood"] > 5 and dict["acient gear"] > 3 and dict["magnetic"] > 3 and not self.railgun:
                        can_make_list.append("railgun") 
                print(f"you can make these {can_make_list}")   
                print()        
                intend = input("What do you want to make \n")
                print()
                if intend == "map":
                    if not self.map:
                        self.map = True
                        self.item_remove("wood", 3)
                        self.item_remove("magnetic", 5)
                        print
                        print("Success!")
                    else:
                        print("you cannot get a second map")
                elif intend == "acient detector": 
                    if not self.acient_detector:
                        self.acient_detector = True
                        self.item_remove("acient gear", 5)
                        self.item_remove("acient core", 1)
                        print("Success!")
                    else:
                        print("having other detectors cannot detect other monsters")
                elif intend == "railgun":
                    if not self.railgun:
                        self.railgun = True
                        self.item_remove("acient gear", 3)
                        self.item_remove("magnetic", 3)
                        self.item_remove("wood", 5)
                        print("Success!")
                    else:
                        print("You cannot use a second railgun! You are not four hand monster!")
                else:
                    print("I cannot craft that, wait for 100 years or try another name")
                print()
                input("Press enter to continue...")
            else:
                print("you have insufficient materials, go explore!")
                print()
                input("Press enter to continue...")
