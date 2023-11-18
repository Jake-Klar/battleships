import os
import game_engine
import random
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
        ships[ship[0:4]] = ship[5:6]
    return ships

#Iterates through each shup and assigns it a location on the board
def place_battleships(board: list, ships: dict, algorithm='simple') -> list:
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
                        if start_loc[1] - j <= 0 or start_loc[1] - j >= 10 or board[start_loc[0]][start_loc[1] - j] is not None:
                            valid_placement = False
                            break
                else:
                    for j in range(int(ships[ship])):
                        if start_loc[0] - j <= 0 or start_loc[0] - j >= 10 or board[start_loc[0] - j][start_loc[1]] is not None:
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

    
    

if __name__ == '__main__':
    #Change this to simple_game_loop to test my singplayer version!
    game_engine.ai_opponent_game_loop()
    