import components
import logging
import os
FORMAT = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='log.txt', format=FORMAT, level=logging.DEBUG)

try:
    path = os.getcwd() + '\\config.txt'
    f = open(path, 'r')
    lines = f.readlines()
    for line in lines:
        if 'size' in line:
            size = int(line[5:])
            logging.info('Size imported as ' + str(size))
        if 'path' in line:
            filename = line[5:]
except FileNotFoundError:
    logging.warning('Was unable to find config file. Continuing with default values (size=10)')
    pass

previous_user_guesses = []

def attack(coordinates: tuple, board: list, ships: dict) -> bool:
    try:
        location = board[coordinates[0]][coordinates[1]]
        if location == None:
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
    while True:
        try:
            x = int(input("Please enter a x co-ordinate "))
            y = int(input("Please enter a y co-ordinate "))
            if (y, x) in previous_user_guesses:
                print("Please enter new co-ordinates that you haven't already")
            elif  x > size - 1 or y > size - 1 or x < 0 or y < 0:
                print("Please enter a value between (inclusive) 0 and", size - 1)
            else:
                previous_user_guesses.append((y, x))
                break
        except ValueError:
            print('Please enter an integer')
            logging.info('Non integer entered at cli_coorindates_input')
        except NameError:
            if x > 9 or y > 9 or x < 0 or y < 0:
                print("Please enter a value between (inclusive) 0 and 9")
            else:
                previous_user_guesses.append((y, x))
                break
    #Flipped due to the formatting nature of a list of lists. The first index is the row (y axis) and the second the column (x axis)
    return (y, x)

def simple_game_loop():
    print("Welcome to Battleships")
    try:
        board, ships = components.initialise_board(size), components.create_battleships(filename)
    except NameError:
        board, ships = components.initialise_board(), components.create_battleships()
    components.place_battleships(board, ships, "simple")
    while True:
        if len(ships) == 0:
            print("Game over")
            break
        print("You will now attack")
        coordinates = cli_coordinates_input()
        if attack(coordinates, board, ships) == True:
            board[coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in ships.items():
                if count == 0:
                    print("Opponents", name, "has been sunk")
                    ships.pop(name)
                    break  
        else:
            print("Miss")
        
        