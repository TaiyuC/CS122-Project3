from item import Item
import os
import random
import time

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
        self.lv = 1
        self.leaving = False

    def __repr__(self):
        return f"you are in {self.world.map[self.loc1][self.loc2]}"
    
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, dir):
        dir = dir.lower()
        if dir == "up" or dir == "north" or dir == "u" or dir == "n":
            whether = self.world.out_of_world_player([self.loc1 - 1,self.loc2])
            if whether:
                self.loc1 -= 1
                return True
        elif dir == "down" or dir == "south" or dir == "d" or dir == "s":
            whether = self.world.out_of_world_player([self.loc1 + 1,self.loc2])
            if whether:
                self.loc1 += 1
                return True
        elif dir == "left" or dir == "l" or dir == "west" or dir == "w":
            whether = self.world.out_of_world_player([self.loc1,self.loc2 - 1])
            if whether:
                self.loc2 -= 1
                return True
        elif dir == "right" or dir == "r" or dir == "east" or dir == "e":
            whether = self.world.out_of_world_player([self.loc1,self.loc2 + 1])
            if whether:
                self.loc2 += 1
                return True
        else:
            return False

    def check_direction(self, dir):
        dir = dir.lower()
        if dir == "up" or dir == "north" or dir == "u" or dir == "n":
            return self.world.out_of_world_player([self.loc1 - 1,self.loc2])
        elif dir == "down" or dir == "south" or dir == "d" or dir == "s":
            return self.world.out_of_world_player([self.loc1 + 1,self.loc2])
        elif dir == "left" or dir == "l" or dir == "west" or dir == "w":
            return self.world.out_of_world_player([self.loc1,self.loc2 - 1])
        elif dir == "right" or dir == "r" or dir == "east" or dir == "e":
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
        ret_dict = {}
        for i in self.items:
            if i.name in ret_dict:
                ret_dict[str(i.name)] += 1
            else:
                ret_dict[str(i.name)] = 1
        for key, value in ret_dict.items():
            print(f"{value} {key}(s)")
        print()
        input("Press enter to continue...")
    
    def kill_monster(self, mon):
        mon.die()
        if mon.name.lower() == "taotie":
            print()
            time.sleep(1)
            print("The world is in peace. You win!") #TODO
            if not self.railgun:
                print("You are a talented and lucky gamer!!")
            self.leaving = True
        else:
            if self.hp < self.maxhp/3:
                print("You are badly injured. Your health is now " + str(self.hp) + ".")
            else:
                print("You win. Your health is now " + str(self.hp) + ".")
            if random.random() < 0.5:
                self.world.item_by_roomtype(self.loc1, self.loc2)
                print("Some material is dropped on the floor")
            else:
                print("Unlucky! No item dropped")


    def attack_monster(self, mon):
        clear()
        print(f"You are attacking {mon.name}: hp {mon.hp}, attack {mon.attack}, defense{mon.defense} ")
        print()
        print("Your health is " + str(self.hp) + ".")
        print()
        Finished = False
        n = 0
        use_gun = True
        while not Finished:
            self.hp -= int(5 ** (mon.attack/self.defense + random.random()))
            mon.hp -= int(5 ** (mon.attack/self.defense + random.random()))
            if self.railgun:
                mon.hp -= 5
            print(f"{n + 1}th round: your HP is {self.hp}, their HP is {mon.hp}")
            if self.hp <= 0:
                print("You lose.")
                self.alive = False
                Finished = True
            elif mon.hp <= 0:
                self.kill_monster(mon)
                Finished = True
            elif self.hp < 15:
                correct_typing = False
                while not correct_typing:
                    print("** You are about to die. Want to run away?")
                    if self.railgun and (mon.hp - 10) < 0:
                        print("(You are too weak to use a railgun!)")
                    inp = input("Yes/No? \n")
                    if inp.lower() == "yes" or inp.lower() == "y":
                        correct_typing = True
                        if random.random() < 0.4 :
                            Finished = True
                            print("You know you won't die! \n")
                        else:
                            print("Monster is chasing you! You are injured! \n")
                            self.hp -= 2
                    elif inp.lower() == "no" or inp.lower() == "n":
                        correct_typing = True
                        print("Bring it on! \n")
                    else:
                        print("** try again, type 'Yes' or 'No' \n")
            elif (mon.hp - 10) < 0:
                if self.railgun:
                    if use_gun:
                        correct_typing = False
                        while not correct_typing:
                            print(f"** charge your railgun and Aim at {mon.name}? (need one turn to charge)")
                            inp = input("Yes/No? \n")
                            if inp.lower() == "yes" or inp.lower() == "y":
                                print("the monster attacks you while you are charging! ")
                                self.hp -= int(5 ** (mon.attack/self.defense - random.random()))
                                correct_typing = True
                                if self.hp > 0:
                                    for _ in range(15):
                                        print("-",end = "")
                                        time.sleep(0.07)
                                    print("/////Boom!\\\\\\\\\\")
                                    time.sleep(0.3)
                                    print("The monster is successfully eliminated")
                                    self.kill_monster(mon)
                                    Finished = True
                                else:
                                    print("You lose.")
                                    self.alive = False
                                    Finished = True
                            elif inp.lower() == "no":
                                print("HAHA, not using a railgun is your battle style!")
                                use_gun = False
                                correct_typing = True
                            else:
                                print("try typing Yes or No")
            n += 1
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

    def inspect_items(self, name):
        for i in self.items:
            if name.lower() == i.name:
                return (i.describe())
            
        return "no such item"

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
                        self.items.append(Item("map", "see where you are, and you can teleport accurately to town with hp recovered", world =""))
                        print("Success! Instruction is updated to help page")
                    else:
                        print("you cannot get a second map")
                elif intend == "acient detector": 
                    if not self.acient_detector:
                        self.acient_detector = True
                        self.item_remove("acient gear", 5)
                        self.item_remove("acient core", 1)
                        self.items.append(Item("acient detector", "see monster's distributions and more detailed statistics", world = ""))
                        print("Success! Instruction is updated to help page")
                    else:
                        print("having other detectors cannot detect not existed monsters")
                elif intend == "railgun":
                    if not self.railgun:
                        self.railgun = True
                        self.item_remove("acient gear", 3)
                        self.item_remove("magnetic", 3)
                        self.item_remove("wood", 5)
                        self.items.append(Item("railgun", "a great tool for battle", world = ""))
                        print("Success! Now you may visit the palace to see whether you can fight against TaoTie")
                    else:
                        print("You cannot have a second railgun! You are not four hand monster!")
                else:
                    print("I cannot craft that, wait for 100 years so it is invented")
                print()
                input("Press enter to continue...")
            else:
                print("you have insufficient materials, go explore!")
                print()
                input("Press enter to continue...")
