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
        "author": "",  # TODO: Your Battlesnake Username
        "color": "#FFD700",  # TODO: Choose color
        "head": "caffeine",  # TODO: Choose head
        "tail": "nr-booster",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    is_move_safe = {
        "up": True,
        "down": True,
        "left": True,
        "right": True
    }

    size = game_state['board']['width']
    snakes = game_state['board']['snakes']
    food = game_state['board']['food']
    snakes[0] = snakes[len(snakes) - 1]

    selfPositions = []

    for segment in game_state["you"]["body"]:
        selfPositions.append(segment)

    selfPositions.pop(len(selfPositions) - 1)
    snakePositions = []
    opponentHeads = []

    for s in snakes:
        opponentHeads.append(s["body"][0])

        for segment in s["body"]:
            snakePositions.append(segment)

    my_head = game_state["you"]["body"][0]  # Coordinates of your head

    Vicinity = False

    # Blanket bad moves
    # dont move out of bounds
    if my_head["x"] == 0:
        is_move_safe["left"] = False

    if my_head["x"] == size - 1:
        is_move_safe["right"] = False

    if my_head["y"] == 0:
        is_move_safe["down"] = False

    if my_head["y"] == size - 1:
        is_move_safe["up"] = False

    # Bodies
    bodies = selfPositions + snakePositions
    if {'x': my_head["x"] - 1, 'y': my_head["y"]} in bodies:
        is_move_safe["left"] = False

    if {'x': my_head["x"] + 1, 'y': my_head["y"]} in bodies:
        is_move_safe["right"] = False

    if {'x': my_head["x"], 'y': my_head["y"] - 1} in bodies:
        is_move_safe["down"] = False

    if {'x': my_head["x"], 'y': my_head["y"] + 1} in bodies:
        is_move_safe["up"] = False

    # Heads and vicinity
    if {'x': my_head["x"] - 1, 'y': my_head["y"]} in opponentHeads \
            or {'x': my_head["x"] - 1, 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"] - 1, 'y': my_head["y"] + 1} in opponentHeads \
            or {'x': my_head["x"] - 2, 'y': my_head["y"]} in opponentHeads \
            or {'x': my_head["x"] - 2, 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"] - 2, 'y': my_head["y"] + 1} in opponentHeads:
        is_move_safe["left"] = False
        Vicinity = True

    if {'x': my_head["x"] + 1, 'y': my_head["y"]} in opponentHeads \
            or {'x': my_head["x"] + 1, 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"] + 1, 'y': my_head["y"] + 1} in opponentHeads \
            or {'x': my_head["x"] + 2, 'y': my_head["y"]} in opponentHeads \
            or {'x': my_head["x"] + 2, 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"] + 2, 'y': my_head["y"] + 1} in opponentHeads:
        is_move_safe["right"] = False
        Vicinity = True

    if {'x': my_head["x"], 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"] - 1, 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"] + 1, 'y': my_head["y"] - 1} in opponentHeads \
            or {'x': my_head["x"], 'y': my_head["y"] - 2} in opponentHeads \
            or {'x': my_head["x"] - 1, 'y': my_head["y"] - 2} in opponentHeads \
            or {'x': my_head["x"] + 1, 'y': my_head["y"] - 2} in opponentHeads:
        is_move_safe["down"] = False
        Vicinity = True

    if {'x': my_head["x"], 'y': my_head["y"] + 1} in opponentHeads \
            or {'x': my_head["x"] - 1, 'y': my_head["y"] + 1} in opponentHeads \
            or {'x': my_head["x"] + 1, 'y': my_head["y"] + 1} in opponentHeads \
            or {'x': my_head["x"], 'y': my_head["y"] + 2} in opponentHeads \
            or {'x': my_head["x"] - 1, 'y': my_head["y"] + 2} in opponentHeads \
            or {'x': my_head["x"] + 1, 'y': my_head["y"] + 2} in opponentHeads:
        is_move_safe["up"] = False
        Vicinity = True

    # If hungry
    print("Vicinity " + str(Vicinity))
    if int(game_state["you"]["health"]) < 50:
        shortest_x = size + 1
        shortest_y = size + 1
        closestFood = food[0]
        for f in food:
            if abs(my_head["x"] - f["x"]) < shortest_x and \
                    abs(my_head["y"] - f["y"]) < shortest_y:
                closestFood = f
                shortest_x = abs(my_head["x"] - f["x"])
                shortest_y = abs(my_head["y"] - f["y"])

        direction = ""

        x_distance = my_head["x"] - closestFood["x"]
        y_distance = my_head["y"] - closestFood["y"]

        print('FINDING FOOD:')
        print('closest is: ' + str(closestFood))
        print('x distance: ' + str(x_distance))
        print('y_distance: ' + str(y_distance))

        if abs(x_distance) > abs(y_distance) or x_distance == 0:
            if y_distance < 0 and is_move_safe["up"]:
                print("food is up")
                direction = "up"
            elif is_move_safe["down"]:
                print("food is down")
                direction = "down"
        elif abs(x_distance) < abs(y_distance) or y_distance == 0:
            if x_distance < 0 and is_move_safe["right"]:
                print("food is right")
                direction = "right"
            elif is_move_safe["left"]:
                print("food is left")
                direction = "left"
        elif abs(x_distance) == abs(y_distance):
            print("diagonal")
            vert = "up" if y_distance < 0 else "down"
            hori = "left" if x_distance > 0 else "right"
            print("hori is " + hori)
            print("vert is " + vert)
            direction = vert if is_move_safe[vert] else hori if is_move_safe[hori] else ""

        if direction == "":
            safe_moves = []
            for move, isSafe in is_move_safe.items():
                if isSafe:
                    safe_moves.append(move)

            if len(safe_moves) == 0:
                return {"move": "down"}

            direction = random.choice(safe_moves)

        print(f"MOVE {game_state['turn']}: {direction}")
        return {"move": direction}

    # IF NOT IN IMMEDIATE DANGER
    elif not Vicinity:
        direction = ""
        my_tail = game_state["you"]["body"][len(game_state["you"]["body"]) - 1]

        x_distance = my_head["x"] - my_tail["x"]
        y_distance = my_head["y"] - my_tail["y"]

        print('FINDING TAIL:')
        print('x distance: ' + str(x_distance))
        print('y_distance: ' + str(y_distance))

        if abs(x_distance) > abs(y_distance):
            if y_distance < 0 and is_move_safe["up"]:
                print("tail is up")
                direction = "up"
            elif is_move_safe["down"]:
                print("tail is down")
                direction = "down"
        elif abs(x_distance) < abs(y_distance):
            if x_distance < 0 and is_move_safe["right"]:
                print("tail is right")
                direction = "right"
            elif is_move_safe["left"]:
                print("tail is left")
                direction = "left"
        elif abs(x_distance) == abs(y_distance):
            print("diagonal")
            vert = "up" if y_distance < 0 else "down"
            hori = "left" if x_distance > 0 else "right"
            print("hori is " + hori)
            print("vert is " + vert)
            direction = vert if is_move_safe[vert] else hori if is_move_safe[hori] else ""

        if direction == "":
            safe_moves = []
            for move, isSafe in is_move_safe.items():
                if isSafe:
                    safe_moves.append(move)

            if len(safe_moves) == 0:
                return {"move": "down"}

            direction = random.choice(safe_moves)

        print(f"MOVE {game_state['turn']}: {direction}")
        return {"move": direction}

    # Throw them off
    elif Vicinity:
        safe_moves = []
        for move, isSafe in is_move_safe.items():
            if isSafe:
                safe_moves.append(move)

        next_move = random.choice(safe_moves) if len(safe_moves) != 0 else "down"

        print(f"MOVE {game_state['turn']}: {next_move}")
        return {"move": next_move}


# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server

    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end
    })
