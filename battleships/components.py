"""Module providing functions on creating necessary game components"""
import os
import random
import json
import logging
import game_engine
import mp_game_engine
FORMAT = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='log.txt', format=FORMAT, level=logging.DEBUG)

def initialise_board(size=10) -> list:
    """Creates a list of lists representing a board
    
    Keyword arguments:
    size -- The length and width of the board, can be set in the config file (default 10)
    """
    try:
        board = [[None for _ in range(size)] for _ in range(size)]
    except TypeError:
        print("A non integer was passed to the size variable")
        logging.debug('Invalid size input provided')
        exit(1)
    return board

def create_battleships(file='battleships.txt') -> dict:
    """Creates a dictionary of battleships and their lengths from a text file

    Keyword arguments:
    filename -- the name of the file that the ship information is found in (default battleships.txt)
    """
    try:
        path = os.getcwd() + '\\' + file
        f = open(path, 'r')
        lines = f.readlines()
        battleships = {}
        for ship in lines:
            battleships[ship[0:4]] = int(ship.partition(":")[2])
    except TypeError:
        print("A non string was passed to the filename variable")
        logging.debug('Filename irregular')
        exit(1)
    except FileNotFoundError:
        print("No ship list file was found with that name. Please check again.")
        logging.debug('Filepath not found error')
        exit(1)
    return battleships

def place_battleships(board: list, ships: dict, algorithm='simple') -> list:
    """Updates the boards to include strings inside that represent the ships

    Keyword arguments:
    board -- the board that is being updated 
    ships -- the list of ships that was created
    algorithm -- defines the type of placement algorithm that will be used (default simple)
    """
    if algorithm == 'simple':
        try:
            k = 0
            for ship in ships:
                for j in range(int(ships[ship])):
                    board[k][j] = ship
                k += 1
        except IndexError:
            print('A ship length exceeds specified board length in battleships.txt')
            logging.warning('Invalid ship lengths set in config file')
            exit(1)
        return board
    elif algorithm == 'random':
        try:
            for ship in ships:
                placed = False
                if random.randint(0, 1) == 0:
                    orientation = "horizontal"
                else:
                    orientation = "vertical"
                while not placed:
                    #Finds suitable start location so there are no overlaps
                    start_loc = (random.randint(0, len(board) - 1), random.randint(0, len(board) - 1))
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
        except IndexError:
            print('A ship length exceeds the specified board length in battleships.txt')
            logging.warning('Invalid ship lengths set in config file')
            exit(1)
        except ValueError:
            print('An issue occured importing the board object')
            logging.debug('Board object not passed correctly')
            exit(1)
        return board
    elif algorithm == 'custom':
        try:
            path = os.getcwd() + r"\placement.json"
            with open(path, 'r') as f:
                placements = json.load(f)
            for ship in placements:
                valid_placement = True
                start_loc = (int(placements[ship][1]), int(placements[ship][0]))
                orientation = placements[ship][2]
                #Places ships based on placements.json
                if orientation == 'h':
                    for j in range(int(ships[ship[0:4]])):
                        if start_loc[1] + j > len(board) - 1 or board[start_loc[0]][start_loc[1] + j] is not None:
                            print("Invalid placements set in your placements file")
                            exit(1)
                else:
                    for j in range(int(ships[ship[0:4]])):
                        if start_loc[0] + j > len(board) - 1 or board[start_loc[0] + j][start_loc[1]] is not None:
                            print("Invalid placements set in your placements file")
                            exit(1)
                for j in range(int(ships[ship[0:4]])):
                    if orientation == 'h':
                        board[start_loc[0]][start_loc[1] + j] = ship[0:4]
                    else:
                        board[start_loc[0] + j][start_loc[1]] = ship[0:4]
        except FileNotFoundError:
            print("placement.json could not be found, please check file is in root directory")
            logging.debug('placement.json file not located in root directory')
            exit(1)
        return board
    else:
        print('Incorrect ship placement algorithm, please change to: Simple, Random or Custom')
        logging.warning('Invalid algorithm provided')
        exit(1)

def place_battleships_flask(board: list, ships: dict, web_data: dict) -> list:
    """Updates the boards to include strings inside that represent the ships for GUI version

    Keyword arguments:
    board -- the board that is being updated
    ships -- list of ships that was created
    web_data -- info from server containing the starting location and orientation of the ships
    
    """
    try:
        for ship in web_data.keys():
            orientation = web_data[ship][2]
            #Places ships based on returned GUI data (start position and length)
            for i in range((int(ships[ship]))):
                if orientation == 'h':
                    board[int(web_data[ship][1])][int(web_data[ship][0]) + i] = ship
                else:
                    board[int(web_data[ship][1]) + i][int(web_data[ship][0])] = ship
        return board
    except ValueError:
        print('Data from GUI recieved incorrectly')
        logging.debug('GUI ship placement information incorrect')
        exit(1)
    except IndexError:
        print('Data from GUI recieved incorrectly')
        logging.debug('Ship placement logic doesnt align with GUI')
        exit(1)
if __name__ == '__main__':
    while True:
        mode = input('To play singleplayer enter s \nTo play multiplayer enter m \n').lower()
        print(mode)
        if mode != 'm' and mode != 's':
            print('Invalid input')
        else:
            break
    if mode == 'm':
        mp_game_engine.ai_opponent_game_loop()
    else:
        game_engine.simple_game_loop()
