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

players = {
    "user": (None, None),
    "ai": (None, None)
}
previous_user_guesses = []
previous_ai_guesses = []

def attack(location: str, ships: dict) -> bool:
    try:
        if location == None:
            return False
        else:
            ships[location] = int(ships[location]) - 1
            return True
    except KeyError:
        print('An error between the ship and board information occured')
        logging.debug('Invalid item found at location on board')
        exit(1)

def cli_coordinates_input() -> tuple:
    while True:
        try:
            x = int(input("Please enter a x co-ordinate "))
            y = int(input("Please enter a y co-ordinate "))
            if (y, x) in previous_user_guesses:
                print("Please enter new co-ordinates that you haven't already")
            elif  x > size - 1 or y > size - 1 or x < 0 or y < 0:
                print("Please enter a value between (inclusive) 0 and", len(players["ai"][0]) - 1)
            else:
                previous_user_guesses.append((y, x))
                break
        except ValueError:
            print('Please enter an integer')
            logging.info('Non integer entered at cli_coordinates_input')
        except NameError:
            if x > 9 or y > 9 or x < 0 or y < 0:
                print("Please enter a value between (inclusive) 0  and 9")
            else:
                previous_user_guesses.append((y, x))
                break
    #Flipped due to the formatting nature of a list of lists. The first index is the row (y axis) and the second the column (x axis)
    return (y, x)

def generate_attack() -> tuple:
    while True:
        try:
            x = random.randint(0, size - 1)
            y = random.randint(0, size - 1)
            if not any ((y, x) == guess for guess in previous_ai_guesses):
                return (y, x)
        except TypeError:
            print('An error occured calculating the size of the users board')
            logging.debug('User board is undefined') 
            exit(1)
        except NameError:
            x = random.randint(0, 9)
            y = random.randint(0, 9)
            if not any ((y, x) == guess for guess in previous_ai_guesses):
                return (y, x)
    
#As I can't alter generate_attack to take differenet arguments per the project specification I have to make a different function for the flask varaition of the game
def generate_attack_flask(previous_ai_guesses_flask) -> tuple:
    while True:
        x = random.randint(0, size - 1)
        y = random.randint(0, size - 1)
        if not any ((y, x) == guess for guess in previous_ai_guesses_flask):
            return (y, x)
 
def ai_opponent_game_loop():
    print("Welcome to Battleships")
    #Initalizing player components
    try:
        players["user"] = components.initialise_board(size), components.create_battleships(filename)
        players["ai"] = components.initialise_board(size), components.create_battleships(filename)
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
        location = players["ai"][0][coordinates[0]][coordinates[1]]
        if attack(location, players["ai"][1]) == True:
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
        #Same as before, but for the User's board
        location = players["user"][0][coordinates[0]][coordinates[1]]
        if attack(location, players["user"][1]) == True:
            players["user"][0][coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in players["user"][1].items():
                if count == 0:
                    print("User's", name, "has been sunk")
                    players["user"][1].pop(name)
                    break
        else:
            print("Miss")
        #Printing User's board at the end of each round
        print("User board:")
        for row in players["user"][0]:
            print(row)