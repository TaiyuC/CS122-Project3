from item import Item
import os
import random
import time

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

class Player:
    def __init__(self, world, hp = 80):
        """initialize the player"""
        self.loc1 = 0 # start in town
        self.loc2 = 0
        self.items = [] 
        self.hp = hp
        self.maxhp = int(self.hp) # for "heal" feature
        self.attack = 7 # atk/def starts 7 but can be imporved as lv goes up
        self.defense = 7
#        self.monster = [] 
        self.alive = True
        self.world = world
        self.map = False #These are 3 main items can be crafted. instead of checking items, I just having these to check which is more convinent to do beta testing
        self.acient_detector = False
        self.railgun = False
        self.lv = 1 # level starts at 1
        self.leaving = False # some winning check. If kills taotie, becomes true

    def __repr__(self):
        """where you are as repr"""
        return f"you are in {self.world.map[self.loc1][self.loc2]}"
    
    # goes in specified direction if possible, returns True
    # if not possible returns False
    def go_direction(self, dir):
        """a lot of short cuts for go direction"""
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
        """check whether a direction can go"""
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
        """go to town"""
        self.hp = self.maxhp
        self.loc1 = 0
        self.loc2 = 0

    def pickup(self, item):
        """add item to inventory"""
        self.items.append(item) 
        item.hold = False 
        item.world.map[item.loc1][item.loc2].remove_item(item)

    def show_inventory(self):
        """printeverything you have in a dictionary"""
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
    
    def level_up(self):
        """become stronger max lv = 10"""
        if self.lv < 10:
            self.lv += 1
            self.attack += 1
            self.defense += 1
            self.maxhp += 5
            self.hp += 5
            return True
        else:
            return False
    
    def kill_monster(self, mon):
        """if it's taotie, end the game, if not, give warning if health is low, and either drop some item or levelup oneself"""
        mon.die()
        if mon.name.lower() == "taotie":
            print()
            time.sleep(1)
            print("The world is in peace. You win!") #TODO
            input("...")
            print("You woke up and discovered it's a dream. 9:00 am, time to study now!")
            if not self.railgun:
                print("You are a talented and lucky gamer!!")
            self.leaving = True
        else:
            if self.hp < self.maxhp/3:
                print("You are badly injured. Your health is " + str(self.hp) + ".")
            else:
                print("You win. Your health is " + str(self.hp) + ".")
            if random.random() < 0.6:
                self.world.item_by_roomtype(self.loc1, self.loc2)
                print("Some material is dropped on the floor")
            else:
                self.level_up()
                print(f"You reached level {self.lv}, your are stronger than before.")


    def attack_monster(self, mon):
        """first give information on you and monster. First reduce hp, and reduce more hp if oneself got a railgun. """
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
            if self.hp <= 0: # die and lose the game
                print("You lose.")
                self.alive = False
                Finished = True
            elif mon.hp <= 0: # if monster died in this process, monster is died
                self.kill_monster(mon)
                Finished = True
            elif self.hp < 15: # let the player choose escape or not
                correct_typing = False # check whether answer is yes or no (y/n)
                while not correct_typing:
                    print("** You are about to die. Want to run away?")
                    if self.railgun and (mon.hp - 10) < 0: # cannot use railgun when hp is low
                        print("(You are too weak to use a railgun!)")
                    inp = input("Yes/No? \n")
                    if inp.lower() == "yes" or inp.lower() == "y":
                        correct_typing = True
                        if random.random() < 0.4 : # have some chance to run away
                            Finished = True
                            print("You know you won't die! \n")
                        else:
                            print("Monster is chasing you! You are injured! \n") # lower hp and may try run again (depending on whether you are killed next turn)
                            self.hp -= 2
                    elif inp.lower() == "no" or inp.lower() == "n": # if the player does not run away
                        correct_typing = True
                        print("Bring it on! \n") 
                    else:
                        print("** try again, type 'Yes' or 'No' \n") # need correct typing
            elif (mon.hp - 10) < 0: # If player hp is high and mon hp is low, 
                if self.railgun: # if one got a railgun, can ask whether or not aim at the monster
                    if use_gun:
                        correct_typing = False
                        while not correct_typing:
                            print(f"** charge your railgun and Aim at {mon.name}? (need one turn to charge, but lower damage is taken)")
                            inp = input("Yes/No? \n")
                            if inp.lower() == "yes" or inp.lower() == "y":
                                print("the monster attacks you while you are charging! ")
                                self.hp -= int(5 ** (mon.attack/self.defense - random.random())) # lower damage is taken while chraging (it's minus)
                                correct_typing = True
                                if self.hp > 0: # some animation when oneself is alive
                                    for _ in range(15):
                                        print("-",end = "")
                                        time.sleep(0.07)
                                    print("/////Boom!\\\\\\\\\\")
                                    time.sleep(0.3)
                                    print("The monster is successfully eliminated")
                                    self.kill_monster(mon)
                                    Finished = True
                                else: # just lose
                                    print("You lose.")
                                    self.alive = False
                                    Finished = True
                            elif inp.lower() == "no": # player does not want to fight
                                print("HAHA, not using a railgun is your battle style!")
                                use_gun = False
                                correct_typing = True
                            else:
                                print("try typing Yes or No") # let the player type again
            n += 1
        print()
        input("Press enter to continue...")
    
    def count_item(self):
        """returns a dictionary of items that player has"""
        ret_dict = {}
        for i in self.items:
            the_name = i.name
            if the_name in ret_dict:
                ret_dict[the_name] += 1
            else:
                ret_dict[the_name] = 1
        return ret_dict

    def inspect_items(self, name):
        """see discription of item"""
        for i in self.items:
            if name.lower() == i.name:
                return (i.describe())
            
        return "no such item"

    def can_craft(self):
        """whether something can be crafted"""
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
        """remove item by name and number"""
        for _ in range(num):
            for i in self.items:
                if i.name == inp_name:
                    self.items.remove(i)

    def make_craft(self):
        if self.map and self.acient_detector and self.railgun: # if get everything crafted
            print("you've made everything")
            print()
            input("Press enter to continue...")
        else:
            if self.can_craft(): #return a list that can be crafted and ask what does the player want to do
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
                intend = input("What do you want to make \n") # Ask what to make, if already has item, print some warning message
                if intend.lower() == "map" or intend.lower() == "m":
                    if not self.map:
                        self.map = True
                        self.item_remove("wood", 3)
                        self.item_remove("magnetic", 5)
                        self.items.append(Item("map", "see where you are, and you can teleport accurately to town with hp recovered", world =""))
                        print("Success! Instruction is updated to help page")
                    else:
                        print("you cannot get a second map")
                elif intend.lower() == "acient detector" or intend.lower() == "ad": 
                    if not self.acient_detector:
                        self.acient_detector = True
                        self.item_remove("acient gear", 5)
                        self.item_remove("acient core", 1)
                        self.items.append(Item("acient detector", "see monster's distributions and more detailed statistics", world = ""))
                        print("Success! Instruction is updated to help page")
                    else:
                        print("You are not an archaeologist, why you need another detector?")
                elif intend.lower() == "railgun" or intend.lower() == "r":
                    if not self.railgun:
                        self.railgun = True
                        self.item_remove("acient gear", 3)
                        self.item_remove("magnetic", 3)
                        self.item_remove("wood", 5)
                        self.items.append(Item("railgun", "a great tool for battle, may need a turn to charge", world = ""))
                        print("Success! Now you have greater strength")
                    else:
                        print("You cannot have a second railgun! You are not four hand monster!")
                else:
                    print("I cannot craft that, wait for 100 years so it is invented") # if the typed item is not correct
                print()
                input("Press enter to continue...")
            else:
                print("you have insufficient materials, go explore!")  # just let the play collect more items and see what can be made. 
                print()
                input("Press enter to continue...")
