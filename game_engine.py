"""Moudle providing fucntions relating to singleplayer gameplay"""
import logging
import os
import components
FORMAT = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='log.txt', format=FORMAT, level=logging.DEBUG)

#Importing variables from the config file
try:
    path = os.getcwd() + '\\config.txt'
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        if 'size' in line:
            SIZE = int(line[5:])
            logging.info('Size imported as ' + str(SIZE))
        if 'path' in line:
            FILE = line[5:]
except FileNotFoundError:
    logging.warning('Was unable to find config file. Continuing with default values (size=10)')
    SIZE = 10
    FILE = 'battleships.txt'

previous_user_guesses = []

def attack(coordinates: tuple, board: list, ships: dict) -> bool:
    """Checks if there is a ship on the board at the provided co-ordinates/index.

    Keyword arguments:
    coordinates -- a representation of the coordinates on the board being checked
    board -- the board that is being checked
    ships -- the dictionary that represents the state of a player's navy
    """
    #Checks to see if a ship was hit, reduces the length if it was
    try:
        location = board[coordinates[0]][coordinates[1]]
        if location is None:
            return False
        else:
            ships[location] = int(ships[location]) - 1
            return True
    except IndexError:
        print('Could not find that location on the board')
        logging.debug('Invalid coordinates made it to the attack functinon')
        exit(1)
    except KeyError:
        print('An erorr between the ship and board infomration occured')
        logging.debug('Invalid item found at location on board')

def cli_coordinates_input() -> tuple:
    """Asks the user for input to create sudo coordinates to be used for an attack"""
    while True:
        try:
            x = int(input("Please enter a x co-ordinate "))
            y = int(input("Please enter a y co-ordinate "))
            if (y, x) in previous_user_guesses:
                print("Please enter new co-ordinates that you haven't already")
            elif  x > SIZE - 1 or y > SIZE - 1 or x < 0 or y < 0:
                print("Please enter a value between (inclusive) 0 and", SIZE - 1)
            else:
                previous_user_guesses.append((y, x))
                break
        except ValueError:
            print('Please enter an integer')
            logging.info('Non integer entered at cli_coorindates_input')
    #Flipped due to the formatting nature of a list of lists
    return (y, x)

def simple_game_loop():
    """Game logic that prompts user to attack until the enemy navy is destroyed"""
    print("Welcome to Battleships Singleplayer")
    #Initializing player components
    try:
        board, ships = components.initialise_board(SIZE), components.create_battleships(FILE)
    except NameError:
        board, ships = components.initialise_board(), components.create_battleships()
    components.place_battleships(board, ships, "simple")
    while True:
        if len(ships) == 0:
            print("Game over")
            break
        print("You will now attack")
        coordinates = cli_coordinates_input()
        if attack(coordinates, board, ships) is True:
            board[coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in ships.items():
                if count == 0:
                    print("Opponents", name, "has been sunk")
                    ships.pop(name)
                    break
        else:
            print("Miss")
