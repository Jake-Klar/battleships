import components
import random
players = {
    "user": (None, None, 'custom'),
    "ai": (None, None, 'random')
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
    #Flipped due to the formatting nature of a list of lists. The first index is the row (y axis) and the second the column (x axis)
    return (y, x)

def generate_attack() -> tuple:
    x = random.randint(0, 9)
    y = random.randint(0, 9)
    #No real need for these to be flipped as they weren't picked with intention, but like... come on they need to be
    return (y, x)
 
def ai_opponent_game_loop():
    finish = False
    print("Welcome to Battleships")
    #Initalizing player components
    players["user"] = components.initialise_board(), components.create_battleships() , 'custom'
    components.place_battleships(players["user"][0], players["user"][1], None, players["user"][2])
    players["ai"] = components.initialise_board(), components.create_battleships(), 'random'
    components.place_battleships(players["ai"][0], players["ai"][1], None, players["ai"][2])
    while True:
        #Checks to see if either player has had all their ships sunk, ends game as a result
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
        for row in players["user"][0]:
            print(row)