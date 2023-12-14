"""Module providing functions relating to multiplayer gameplay"""
import random
import logging
import os
FORMAT = '%(levelname)s: %(asctime)s %(message)s'
logging.basicConfig(filename='log.txt', format=FORMAT, level=logging.DEBUG)

try:
    import components
except ModuleNotFoundError:
    print('Components module not found. Ensure it is in the root directory')
    logging.debug('Components module not found')
    exit(1)

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
        if 'algorithm' in line:
            ALGORITHM = line[10:].strip('\n')
            logging.info('Algorithm imported as ' + ALGORITHM)
except FileNotFoundError:
    logging.warning('Was unable to find config file. Continuing with default values (size=10)')
    SIZE = 10
    FILE = 'battleships.txt'
except ValueError:
    logging.warning('Improperly configured config file. Continuing with default values')
    print('Config file missing data. Game will continue with default values')
    SIZE=10
    FILE='battleships.txt'

players = {
    "user": (None, None),
    "ai": (None, None)
}
previous_user_guesses = []
previous_ai_guesses = []

def attack(coordinates: tuple, board: list, ships: dict) -> bool:
    """Checks if there is a ship on the board at the provided co-ordinates/index.

    Keyword arguments: 
    coordinates -- a representation of the coordinates on the board being checked
    board -- the board that is being checked
    ships -- the dictionary that represents the state of a player's navy
    """
    try:
        location = board[coordinates[0]][coordinates[1]]
        if location is None:
            return False
        else:
            ships[location] = int(ships[location]) - 1
            return True
    except KeyError:
        print('An error between the ship and board information occured')
        logging.debug('Invalid item found at location on board')
        exit(1)

def cli_coordinates_input() -> tuple:
    """Asks the user for input to create sudo coordiantes to be used for an attack"""
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
            logging.info('Non integer entered at cli_coordinates_input')
    #Flipped due to the formatting nature of a list of lists.
    return (y, x)

def generate_attack() -> tuple:
    """Randomly generates coordiantes for use in the AI's attack"""
    while True:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if (y, x) not in previous_ai_guesses:
            return (y, x)

#As I can't alter generate_attack to take different arguments per the project specification
#I have to make a different function for the flask varaition of the game
def generate_attack_flask(previous_ai_guesses_flask) -> tuple:
    """Randomly generates coordinates for use in the Ai's attack (specifically for flask)
    
    Keyword arguments:
    previous_ai_guesses_flask -- provided from main.py, a list of previous AI guesses
    """
    while True:
        x = random.randint(0, SIZE - 1)
        y = random.randint(0, SIZE - 1)
        if not any ((y, x) == guess for guess in previous_ai_guesses_flask):
            return (y, x)

def ai_opponent_game_loop() -> None:
    """Game logic that handles user and AI attacks until either's navy has been destroyed"""
    print("Welcome to Battleships Multiplayer")
    #Initalizing player components
    try:
        players["user"] = components.initialise_board(SIZE), components.create_battleships(FILE)
        players["ai"] = components.initialise_board(SIZE), components.create_battleships(FILE)
        components.place_battleships(players["user"][0], players["user"][1], ALGORITHM)
        components.place_battleships(players["ai"][0], players["ai"][1], 'random')
    except NameError:
        players["user"] = components.initialise_board(), components.create_battleships()
        players["ai"] = components.initialise_board(), components.create_battleships()
        components.place_battleships(players["user"][0], players["user"][1], 'custom')
        components.place_battleships(players["ai"][0], players["ai"][1], 'random')
    while True:
        #Checks to see if either player has had all their ships sunk, ends game as a result
        for player, data in players.items():
            if len(data[1]) == 0:
                print(player, "has lost")
                exit(1)
        #User attack
        print("The user will now attack")
        coordinates = cli_coordinates_input()
        if attack((coordinates[0], coordinates[1]), players["ai"][0], players["ai"][1]) is True:
            players["ai"][0][coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in players["ai"][1].items():
                if count == 0:
                    print("AI's", name, "has been sunk")
                    players["ai"][1].pop(name)
                    break
        else:
            print("Miss")
        #AI Attack
        print("The ai will now attack")
        coordinates = generate_attack()
        if attack((coordinates[0], coordinates[1]), players["user"][0], players["user"][1]) is True:
            players["user"][0][coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in players["user"][1].items():
                if count == 0:
                    print("User's", name, "has been sunk")
                    players["user"][1].pop(name)
                    break
        else:
            print("Miss")
        print("User board:")
        for row in players["user"][0]:
            print(row)
