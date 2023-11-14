import os
import game_engine
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
        ships[ship[0:5]] = ship[6:7]
    return ships

#Iterates through each shup and assigns it a location on the board
def place_battleships(board: list, ships: dict, algorithm='simple') -> list:
    if algorithm == 'simple':
        k = 0
        for i in ships:
            for j in range(int(ships[i])):
                board[k][j] = i
            k += 1
        return board

if __name__ == '__main__':
    game_engine.ai_opponent_game_loop()
    

