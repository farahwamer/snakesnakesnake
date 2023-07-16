# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "farahwamer",  # TODO: Your Battlesnake Username
        "color": "#888888",  # TODO: Choose color
        "head": "default",  # TODO: Choose head
        "tail": "default",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")

def prevent_out_of_bounds(width, height, head, is_move_safe):
    if head["x"] == width - 1:
        is_move_safe["right"] = False
    if head["x"] == 0:
        is_move_safe["left"] = False
    if head["y"] == height - 1:
        is_move_safe["up"] = False
    if head["y"] == 0:
        is_move_safe["down"] = False

def prevent_self_collision(body, head, is_move_safe):
    if {"x": head["x"] + 1, "y": head["y"]} in body:
        is_move_safe["right"] = False
    if {"x": head["x"] - 1, "y": head["y"]} in body:
        is_move_safe["left"] = False
    if {"x": head["x"], "y": head["y"] + 1} in body:
        is_move_safe["up"] = False
    if {"x": head["x"], "y": head["y"] - 1} in body:
        is_move_safe["down"] = False

def prevent_collision_with_body(body, my_head, is_move_safe):
    if {"x": my_head["x"] + 1, "y": my_head["y"]} in body:
        is_move_safe["right"] = False
    if {"x": my_head["x"] - 1, "y": my_head["y"]} in body:
        is_move_safe["left"] = False
    if {"x": my_head["x"], "y": my_head["y"] + 1} in body:
        is_move_safe["up"] = False
    if {"x": my_head["x"], "y": my_head["y"] - 1} in body:
        is_move_safe["down"] = False

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False

    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False

    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False

    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Step 1 - Prevent your Battlesnake from moving out of bounds
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']

    prevent_out_of_bounds(board_width, board_height, my_head, is_move_safe)

    # TODO: Step 2 - Prevent your Battlesnake from colliding with itself
    my_body = game_state['you']['body']
 
    # prevent_self_collision(my_body, my_head, is_move_safe)
    prevent_collision_with_body(my_body, my_head, is_move_safe)

    # TODO: Step 3 - Prevent your Battlesnake from colliding with other Battlesnakes
    opponents = game_state['board']['snakes']

    for snake in opponents:
        prevent_collision_with_body(snake["body"], my_head, is_move_safe)
        print(snake)

    # Are there any safe moves left?
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}
    
    # Choose a random move from the safe ones
    next_move = random.choice(safe_moves)
    print(f"snake head at: {my_head}, safe moves: {safe_moves}")
    # TODO: Step 4 - Move towards food instead of random, to regain health and survive longer
    # food = game_state['board']['food']

    print(f"MOVE {game_state['turn']}: {next_move}")
    return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({"info": info, "start": start, "move": move, "end": end})


# STRATEGY NOTES
# we should add a check to avoid having the snake make a loop on itself