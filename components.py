import os
import game_engine
import mp_game_engine
import random
import json
#Creates an empty board state taking an integer as an argument for the size of the board
def initialise_board(size=10) -> list:
    board = [[None for _ in range(size)] for _ in range(size)]
    return board

#Reads a file to get ship names and sizes, please make sure the folder is located under you user folder i.e C:\Users\your name otherwise it won't work (at least assuming you're running in VSCode
# like I was, otherwise I'm not sure what your programs cwd will be)
def create_battleships(filename=r'\battleships.txt') -> dict:
    path = os.getcwd() + r"\battleships" + filename
    f = open(path, 'r')
    lines = f.readlines()
    ships = {}
    for ship in lines:
        ships[ship[0:4]] = int(ship[5:6])
    return ships

#Iterates through each shup and assigns it a location on the board. Web ver decides if I'm reading the placement.json file for the CLI game or using the response from my server for the multiplayer game
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
            path = os.getcwd() + r"\battleships" + r"\placement.json"
            with open(path, 'r') as f:
                """Change it if you wish, but it's currently set to saying HI which is cool. If you do change it, the ships are built upwards from start if orientation is vertical
                and left from the start if the orientation is horizontal"""
                placements = json.load(f)
            for ship in placements:
                valid_placement = True
                start_loc = (int(placements[ship][0]), int(placements[ship][1]))
                orientation = placements[ship][2]
                if orientation == 'h':
                    for j in range(int(ships[ship[0:4]])):
                        if start_loc[1] + j < 0 or board[start_loc[0]][start_loc[1] - j] is not None:
                            print("Invalid placements set. Please update to avoid going out of bounds or overlapping ships. Remember ships are built upwards from start location or left from start location")
                            valid_placement = False
                            exit(1)
                else:
                    for j in range(int(ships[ship[0:4]])):
                        if start_loc[0] - j < 0 or board[start_loc[0] - j][start_loc[1]] is not None:
                            print("Invalid placements set. Please update to avoid going out of bounds or overlapping ships. Remember ships are built upwards from start location or left from start location")
                            valid_placement = False
                            exit(1)
                if valid_placement:
                    for j in range(int(ships[ship[0:4]])):
                        if orientation == 'h':
                            board[start_loc[0]][start_loc[1] - j] = ship[0:4]
                        else:
                            board[start_loc[0] - j][start_loc[1]] = ship[0:4]
            return board
    elif algorithm == 'web':
        for ship in web_data.keys():
            orientation = web_data[ship][2]
            for i in range((int(ships[ship]))):
                if orientation == 'h':
                    board[int(web_data[ship][1])][int(web_data[ship][0]) + i] = ship
                else:
                     board[int(web_data[ship][1]) + i][int(web_data[ship][0])] = ship 
        return board
    
if __name__ == '__main__':
    #Change this to simple_game_loop to test my singplayer version!
    mp_game_engine.ai_opponent_game_loop()
    