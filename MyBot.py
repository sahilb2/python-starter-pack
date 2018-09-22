# keep these three import statements
import game_API
import fileinput
import json

# your import statements here
import random

first_line = True # DO NOT REMOVE

# global variables or other functions can go here
stances = ["Rock", "Paper", "Scissors"]

nodes_map = {}
nodes_map[0] = [1, 6, 10]
nodes_map[1] = [3, 0]
nodes_map[3] = [1]
nodes_map[6] = [0]
nodes_map[10] = [0, 16]
nodes_map[16] = [10]

def get_winning_stance(stance):
    if stance == "Rock":
        return "Paper"
    elif stance == "Paper":
        return "Scissors"
    elif stance == "Scissors":
        return "Rock"

def get_next_node(me, game):
    if me.location == me.destination:
        if game.has_monster(me.location) and (game.get_monster(me.location).respawn_counter < 0.2 * game.get_monster(me.location).respawn_rate):
            return me.location
        next_nodes = nodes_map[me.location]
        if 0 in next_nodes:
            if not game.get_monster(0).dead or (game.get_monster(0).respawn_counter < 0.3 * game.get_monster(0).respawn_rate):
                return 0
        for node in next_nodes:
            if game.has_monster(node):
                monster = game.get_monster(node)
                if not monster.dead or (monster.respawn_counter < 0.2 * monster.respawn_rate):
                    if me.location == 0:
                        nodes_map[0] = next_nodes[::-1]
                        if me.scissors < 3:
                            temp = nodes_map[0][0]
                            nodes_map[0][0] = nodes_map[0][1]
                            nodes_map[0][1] = temp
                    return node
        if me.location == 1:
            return 0
        return next_nodes[0]
    elif me.destination == -1:
        return 0
    else:
        return me.destination

def get_next_stance(me, game):
    if game.has_monster(me.location):
        monster = game.get_monster(me.location)
        if not monster.dead:
            return get_winning_stance(monster.stance)
    opponent = game.get_opponent()
    if opponent.stance == "Invalid Stance":
        return "Paper"
    return get_winning_stance(opponent.stance)


# main player script logic
# DO NOT CHANGE BELOW ----------------------------
for line in fileinput.input():
    if first_line:
        game = game_API.Game(json.loads(line))
        first_line = False
        continue
    game.update(json.loads(line))
# DO NOT CHANGE ABOVE ---------------------------

    # code in this block will be executed each turn of the game

    me = game.get_self()

    destination_node = get_next_node(me, game)
    chosen_stance = get_next_stance(me, game)

    # submit your decision for the turn (This function should be called exactly once per turn)
    game.submit_decision(destination_node, chosen_stance)
