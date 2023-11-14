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
    finish = False
    print("Welcome to Battleships")
    for player in players:
        players[player] = (components.initialise_board(), components.create_battleships())
        components.place_battleships(players[player][0], players[player][1])
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
                    print("Opponents", name, "has been sunk")
                    ships.pop(name)
                    break  
        else:
            print("Miss")
        
        