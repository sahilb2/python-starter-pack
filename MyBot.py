# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # do not remove

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

# main player script logic
for line in fileinput.input(): # loop over each line of input
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))

    # ----------YOUR CODE BELOW----------
    # this code will be executed each turn of the game

    me = game.get_self()
    nearest_monsters = game.nearest_monsters(me.location, 1)
    paths = game.shortest_paths(me.location, nearest_monsters[0].location)
    destination_node = paths[0][0]

    chosen_stance = stances[random.randint(0, 2)]

    game.submit_decision(destination_node, chosen_stance)
