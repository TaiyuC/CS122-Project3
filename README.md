## Read me

To run this project, download the folder "this_is_the_project3" and type:

```
% python3 MAIN16.py
```
# Improvements made:

1. (Bigger world and random world) rewrite format of room, and adding a class "World", so now world can be any size(even though in game player do not choose the size of the world, but by changing the number we can get a squared bigger world). Randomly generated room based on three main types are also happened here. In dessert there is one material called acient core which is unique, so at least one super monster is there. 
2. me command, there are surpirses when using me command multiple times as well
3. inspect/ insp command
4. regeneration: by heal command/ teleport command
5. Loot: defeat a monster causes item to appear or level up.(random). Also, created mechanism that need to defeat monster in that area to pickup.
6. More Monsters: monsters originated in acient Chinese book is added, and stronger monsters are a subclass of the monsters. There is also a boss like monster to defeat.
7. Player attribute: defense, attack... 
8. Weapon: only one weapon is added, which assists the battle process.
9. Victory condition: defeat the final boss
10. Command abbreviations: monster abbreviation, command abbreviation, direction abbreviation.
11. level up: level up with higher attack, defense and hp.
12. craft: all things picked up are marterials. Can craft three types of item using the materials. map, railgun, detector. Also interactive, only can what can be made if get enough materials. need to type what is the thing want to make
13. teleport: can go to random direction without map, but with map can go back to town with full hp.
14. go direction: if map is unlocked, can go multiple directions in single line. (like go up down left north u d r) will first check whether it goes successfully, if not go random direction, but if yes, just can go there more quickly.
15. see monster status: see statistics of monster; if there is a detector, see more detailed statistics.
16. introduction: some introduction words before entering the game.
17. inventory: show inventory
18. update only on normal monster. super monster do not update themselves.
19. battle system is improved a little: might be able to run away when hp is low, and can use charged railgun to finish battle.
