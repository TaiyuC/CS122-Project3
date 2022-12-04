from ROOM16 import Room
from player import Player
from item import Item
from monster import Monster
from world import World
import os
import updater
import random

def create_world():
    w = World(6)
    w.generate_monsters(30)
    w.initialize_item()
    
    return w

w = create_world()
player = Player(world= w, hp= 100)

# player.railgun = True
# player.acient_detector = True
# player.map = True

# for _ in range(10):  #this is just for beta testing
#     wo = Item(name = "wood", desc = "we may use wood to make something", world = w)
#     w.map[0][0].add_item(wo)
#     wo.put_in_loc([0,0])
#     ag = Item(name = "acient gear", desc = "we may use acient gear to make something", world = w)
#     w.map[0][0].add_item(ag)
#     ag.put_in_loc([0,0])
#     ma = Item(name = "magnetic", desc = "we may use magnetic to make something", world = w)
#     w.map[0][0].add_item(ma)
#     ma.put_in_loc([0,0])
#     ac = Item(name = "acient core", desc = "bla", world = w)
#     ac.put_in_loc([0,0])
#     w.map[0][0].add_item(ac)
#     player.pickup(wo)
#     player.pickup(ma)
#     player.pickup(ag)
#     player.pickup(ac)
#     # #######pickup wood
#     # #######pickup magnetic
#     # #######pickup acient gear

# items_can_make = [Item(name = "map", desc = "can see the world by map command", world = w), 
#                   Item(name = "acient detector", desc = "can see statistics of monsters", world = w),
#                   Item(name = "railgun", desc = "increases attack", world = w)]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def introduction():
    clear()
    print("Welcome to the world, ")

def player_status():
    clear()
    print(f"Your hp is {player.hp}, you are {player.loc1 + player.loc2} move(s) away from town")
    if random.random() < 0.2:
        print()
        if not player.map:
            print("You remenbered you learned from KongFu master that making a map needs 3 woods and 5 magnetics")
        elif not player.acient_detector:
            print("You remenbered an archaeologist says one acient core and some acient gears is how people used to make detectors")
        elif not player.railgun:
            print("You just realized there is an acient tale, in which ancestors defeated TaoTie together by combining powers of mountain, desert, and forest")
        else:
            print("It's time to stop TaoTie")
    if player.acient_detector or player.railgun or player.map:
        print()
        crafted = []
        if player.acient_detector:
            crafted.append("acient_detector")
        if player.railgun:
            crafted.append("railgun")
        if player.map:
            crafted.append("map")
        crafted_message = "You currently have: "
        for object in crafted:
            crafted_message += (str(object) + ", ")
        print(f"{crafted_message[:-2]}.")
    print()
    input("Press enter to continue...")

def print_situation():
    clear()
    cur_room = player.world.map[player.loc1] [player.loc2]
    cur_room_str = str(player.world.map[player.loc1] [player.loc2]).replace("_", "", -1)
    print("-------------------------")
    print(f"you are at {cur_room_str}")
    print()
    if cur_room.has_monsters():
        print("This room contains the following monsters:")
        for m in cur_room.monsters:
            print(m.name)
        print()
    if cur_room.has_items():
        print("This room contains the following items:")
        for i in cur_room.items:
            print(i.name)
        print()
    print("You can go in the following directions:")
    for dir in ["up", "down", "left", "right"]:
        if player.check_direction(dir):
            print(dir)
    print()

def heal_at_town():
    clear()
    if player.loc1 == 0 and player.loc2 == 0:
        if player.hp == player.maxhp:
            print("Healing stone is not responding...")
        else:
            player.hp = player.maxhp
            print("You are good to go!")
    else:
        print("Go back to town and try again! ")
    print()
    input("Press enter to continue...")

def show_help():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    if not player.map:
        print("teleport -- just moves you to a random location")
    else:
        print("teleport -- go back to town with full hp")
    print("heal -- there is a healing stone in town")
    if not (player.acient_detector and player.map and player.railgun):
        print("craft -- craft something to help you, try to get more materials to see items can be crafted")
    print("attack <monster name> -- fight with monster")
    if player.map:
        print("map -- see the whole world and where you are. leftup corner is [0,0]")
    if player.acient_detector:
        print("detect -- see more accurate and detailed monster statistics and distribution when having a detector")
    else:
        print("detect -- see some statistics about monsters, craft a detector to imporve this feature")
    if player.railgun:
        print("(You are carrying railgun)")
    print("exit -- quits the game")
    print()
    input("Press enter to continue...")

def show_map():
    clear()
    if player.map:
        print(f"you are at {[player.loc1,player.loc2]}")
        w.view()
    else:
        print("you do not have a map")
    print()
    input("Press enter to continue...")

def view_mon():
    clear()
    print("________________")
    if player.acient_detector:
        mon_dict, mon_list = w.view_monster()
        print(f"count by type of land:{mon_dict}")
        for name in mon_list:
            print(f"{name}")
    else:
        print("Since you do not have detector, this is all you can check")
        mon_list = w.glimpse_monster()
        for name in mon_list:
            print(f"{name}")
    print()
    input("Press enter to continue...")

def teleport():
    clear()
    if player.map:
        print(f"your hp {player.hp} is fully recovered and you are back to town")
        player.teleport()
    else:
        print("Oops, you do not have a map so you are lost")
        [player.loc1,player.loc2] = w.monster_loc()
    print()
    input("Press enter to continue...")

def pick_up():
    clear()
    if w.w_has_monster([player.loc1,player.loc2]):
        print("Monster is watching you, be careful")
        print()
        input("Press enter to continue...")
    else:
        target_name = command[7:] # everything after "pickup "
        target = w.map[player.loc1][player.loc2].get_item_by_name(target_name)
        if target != False:
            player.pickup(target)
            print(f"{target_name} get!")
        else:
            print("No such item.")
            command_success = False
        print()
        input("Press enter to continue...")

def inspection(word):
    clear()
    print(player.inspect_items(word))
    print()
    input("Press enter to continue...") 

if __name__ == "__main__":
    playing = True
    while playing and player.alive:
        print_situation()
        command_success = False
        time_passes = False
        while not command_success:
            command_success = True
            command = input("What now? ")
            if len(command) == 0:
                continue
            command_words = command.split()
            if len(command_words) == 0:
                continue
            match command_words[0].lower():
                case "go":   #cannot handle multi-word directions
                    okay = player.go_direction(command_words[1]) 
                    if okay:
                        time_passes = True
                    else:
                        print("You can't go that way.")
                        command_success = False
                case "teleport":
                    teleport()
                case "me":
                    player_status()
                case "map":
                    show_map()
                case "detect":
                    view_mon()
                case "pickup":  #can handle multi-word objects
                    pick_up()
                case "inventory":
                    player.show_inventory()
                case "craft":
                    player.make_craft()
                case "help":
                    show_help()
                case "exit":
                    playing = False
                case "heal":
                    heal_at_town()
                case "attack":
                    target_name = command[7:]
                    target = player.world.map[player.loc1][player.loc2].get_monster_by_name(target_name)
                    if target != False:
                        player.attack_monster(target)
                    else:
                        print("No such monster.")
                        command_success = False
                case "inspect":
                    inspection(command[8:])
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            if random.random() < 0.3:
                updater.update_all()
            if random.random() < 0.2:
                w.item_new()
                w.mon_new()
