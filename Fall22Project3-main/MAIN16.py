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
    return w

w = create_world()

player = Player(world= w, hp= 100)

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
    print("quit -- quits the game")
    print()
    input("Press enter to continue...")

def show_map():
    clear()
    print(f"you are at {[player.loc1,player.loc2]}")
    w.view()
    print()
    input("Press enter to continue...")

def view_mon():
    clear()
    mon_dict, mon_list = w.view_monster()
    print(f"count by type of land:{mon_dict}")
    print(f"list of names: {mon_list}")
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
                case "where":
                    show_map()
                case "mon":
                    view_mon()
                # case "pickup":  #can handle multi-word objects
                #     target_name = command[7:] # everything after "pickup "
                #     target = player.location.get_item_by_name(target_name)
                #     if target != False:
                #         player.pickup(target)
                #     else:
                #         print("No such item.")
                #         command_success = False
                # case "inventory":
                #     player.show_inventory()
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