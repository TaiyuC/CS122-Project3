from ROOM16 import Room
from player import Player
from item import Item
from monster import Monster
from world import World
import os
import updater


def create_world():
    w = World(5)
    w.generate_monsters(10)
    w.initialize_item()
    
    return w

w = create_world()
player = Player(world= w, hp= 100)
for _ in range(10):  #this is just for beta testing
    wo = Item(name = "wood", desc = "we may use wood to make something", world = w)
    w.map[0][0].add_item(wo)
    wo.put_in_loc([0,0])
    ag = Item(name = "acient gear", desc = "we may use acient gear to make something", world = w)
    w.map[0][0].add_item(ag)
    ag.put_in_loc([0,0])
    ma = Item(name = "magnetic", desc = "we may use magnetic to make something", world = w)
    w.map[0][0].add_item(ma)
    ma.put_in_loc([0,0])
    player.pickup(wo)
    player.pickup(ma)
    player.pickup(ag)
#pickup wood
#pickup magnetic
#pickup acient gear
# items_can_make = [Item(name = "map", desc = "can see the world by map command", world = w), 
#                   Item(name = "acient detector", desc = "can see statistics of monsters", world = w),
#                   Item(name = "railgun", desc = "increases attack", world = w)]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_situation():
    clear()
    cur_room = player.world.map[player.loc1] [player.loc2]
    print(f"you are at {cur_room}")
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


def show_help():
    clear()
    print("go <direction> -- moves you in the given direction")
    print("inventory -- opens your inventory")
    print("pickup <item> -- picks up the item")
    print("exit -- quits the game")
    print("teleport -- go back to town with full hp if you have map")
    print("craft -- craft something to help you")
    crafted = []
    if player.acient_detector:
        crafted.append("acient_detector")
    if player.railgun:
        crafted.append("railgun")
    if player.map:
        crafted.append("map")
    for object in crafted:
        print(f"you now have {object}")
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
    if player.acient_detector:
        mon_dict, mon_list = w.view_monster()
        print(f"count by type of land:{mon_dict}")
        print(f"list of names: {mon_list}")
    else:
        print("you do not have any detector")
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
                case "map":
                    show_map()
                case "mon":
                    view_mon()
                case "pickup":  #can handle multi-word objects
                    target_name = command[7:] # everything after "pickup "
                    target = w.map[player.loc1][player.loc2].get_item_by_name(target_name)
                    if target != False:
                        player.pickup(target)
                    else:
                        print("No such item.")
                        command_success = False
                case "inventory":
                    player.show_inventory()
                case "craft":
                    player.make_craft()
                case "help":
                    show_help()
                case "exit":
                    playing = False
                case "attack":
                    target_name = command[7:]
                    target = player.world.map[player.loc1][player.loc2].get_monster_by_name(target_name)
                    if target != False:
                        player.attack_monster(target)
                    else:
                        print("No such monster.")
                        command_success = False
                case other:
                    print("Not a valid command")
                    command_success = False
        if time_passes == True:
            updater.update_all()
