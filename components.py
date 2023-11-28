import os
import game_engine
import mp_game_engine
import random
import json

#Creates an empty board state taking an integer as an argument for the size of the board
def initialise_board(size=10) -> list:
    board = [[None for _ in range(size)] for _ in range(size)]
    return board

#If this is returning an error it's because your current working directory isn't the battleships folder. Please change your CWD to that.
def create_battleships(filename=r'\battleships.txt') -> dict:
    path = os.getcwd() + filename
    f = open(path, 'r')
    lines = f.readlines()
    ships = {}
    for ship in lines:
        ships[ship[0:4]] = int(ship.partition(":")[2])
    return ships

#Web_data is only used for when the game is using FLASk and it's to give the algorithm the users chosen placement data
def place_battleships(board: list, ships: dict, web_data: dict, algorithm='simple') -> list:
    if algorithm == 'simple':
        k = 0
        for ship in ships:
            for j in range(int(ships[ship])):
                board[k][j] = ship
            k += 1
        return board
    elif algorithm == 'random':
        for ship in ships:
            placed = False
            if random.randint(0, 1) == 0:
                orientation = "horizontal"
            else:
                orientation = "vertical"
            while not placed:
                #Tries to place a ship in its randomly chosen orientation until it finds a suitable location and then moves onto the next ship
                start_loc = (random.randint(0, 9), random.randint(0, 9))
                valid_placement = True  
                if orientation == "horizontal":
                    for j in range(int(ships[ship])):
                        if start_loc[1] - j < 0 or board[start_loc[0]][start_loc[1] - j] is not None:
                            valid_placement = False
                            break
                else:
                    for j in range(int(ships[ship])):
                        if start_loc[0] - j < 0 or board[start_loc[0] - j][start_loc[1]] is not None:
                            valid_placement = False
                            break
                if valid_placement:
                    for j in range(int(ships[ship])):
                        if orientation == "horizontal":
                            board[start_loc[0]][start_loc[1] - j] = ship
                        else:
                            board[start_loc[0] - j][start_loc[1]] = ship
                    placed = True
        return board
    elif algorithm == 'custom':
            path = os.getcwd() + r"\placement.json"
            with open(path, 'r') as f:
                placements = json.load(f)
            for ship in placements:
                valid_placement = True
                #Flipped due to the formatting nature of a list of lists. The first index is the row (y axis) and the second the column (x axis)
                start_loc = (int(placements[ship][1]), int(placements[ship][0]))
                orientation = placements[ship][2]
                #Tests for the orientation given if the ship is either a) Out of bounds or b) Overlapping with another ship
                if orientation == 'h':
                    for j in range(int(ships[ship[0:4]])):
                        if start_loc[1] + j > 9 or board[start_loc[0]][start_loc[1] + j] is not None:
                            print("Invalid placements set. Please update to avoid going out of bounds or overlapping ships")
                            exit(1)
                else:
                    for j in range(int(ships[ship[0:4]])):
                        if start_loc[0] + j > 9 or board[start_loc[0] + j][start_loc[1]] is not None:
                            print("Invalid placements set. Please update to avoid going out of bounds or overlapping ships")
                            exit(1)
                for j in range(int(ships[ship[0:4]])):
                    if orientation == 'h':
                        board[start_loc[0]][start_loc[1] + j] = ship[0:4]
                    else:
                        board[start_loc[0] + j][start_loc[1]] = ship[0:4]
            return board
    elif algorithm == 'web':
        for ship in web_data.keys():
            orientation = web_data[ship][2]
            #Similar to the custom placement, but we don't need to do checks on ship placement as the frontend handles it for us
            for i in range((int(ships[ship]))):
                if orientation == 'h':
                    board[int(web_data[ship][1])][int(web_data[ship][0]) + i] = ship
                else:
                     board[int(web_data[ship][1]) + i][int(web_data[ship][0])] = ship 
        return board
    
if __name__ == '__main__':
    #Change this to simple_game_loop to test my singplayer version!
    mp_game_engine.ai_opponent_game_loop()
    