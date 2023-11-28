import components

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

def simple_game_loop():
    print("Welcome to Battleships")
    board, ships = components.initialise_board(), components.create_battleships()
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
        
        