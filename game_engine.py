import components
import random
players = {

    "user": None,
    "ai": None
}

def attack(location: str, ships: dict) -> bool:
    if location == None:
        return False
    else:
        ships[location] = int(ships[location]) - 1
        return True

def cli_coordinates_input() -> tuple:
    x = int(input("Please enter a x co-ordinate "))
    y = int(input("Please enter a y co-ordinate "))
    return (x, y)

def generate_attack() -> tuple:
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    return (x, y)

#Todo. Rewrite whole thing into a for loop with board and ships initalized inside the dictionary. 
def ai_opponent_game_loop():
    print("Welcome to Battleships")
    user_board, user_ships = components.initialise_board(), components.create_battleships()
    ai_board, ai_ships = components.initialise_board(), components.create_battleships()
    players["user"] = (user_board, user_ships)
    players["ai"] = (ai_board, ai_ships)
    for data in players.values():
        components.place_battleships(data[0], data[1])
    while True:
        for player, data in players.items():
            if len(data[1]) == 0:
                print(player, " has lost")
                finish = True
        if finish == True:
            break
        #User attack
        print("The user will now attack")
        coordinates = cli_coordinates_input()
        #This line could be hard to follow. Basically setting location to the AI's board at the coordinates provided
        #I needed to specify the variable as _ai otherwise I'd be updating the users board at that position on the second run through
        location_ai = ai_board[coordinates[0]][coordinates[1]]
        if attack(location_ai, ai_ships) == True:
            ai_board[coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in ai_ships.items():
                if count == 0:
                    print(name, "has been sunk")
                    ai_ships.pop(name)
                    break
        else: 
            print("Miss")
        #AI Attack
        print("The ai will now attack")
        coordinates = generate_attack()
        #Same as before, but for the User's board
        location = user_board[coordinates[0]][coordinates[1]]
        if attack(location, user_ships) == True:
            user_board[coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in user_ships.items():
                if count == 0:
                    print(name, "has been sunk")
                    user_ships.pop(name)
                    break
        else:
            print("Miss")


def simple_game_loop():
    print("Welcome to Battleships")
    board = components.initialise_board()
    ships = components.create_battleships()
    components.place_battleships(board, ships)
    while True:
        if len(ships) == 0:
            print("Game over")
            break
        print("You will now attack")
        coordinates = cli_coordinates_input()
        location = board[coordinates[0]][coordinates[1]]
        if attack(location, ships) == True:
            board[coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in ships.items():
                if count == 0:
                    print(name, "has been sunk")
                    ships.pop(name)
                    break  
        else:
            print("Miss")
        
        