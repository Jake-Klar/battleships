import components

def attack(coordinates: tuple, board: list, ships: dict) -> bool:
    location = board[coordinates[0]][coordinates[1]]
    if location == None:
        return False
    else:
        ships[location] = int(ships[location]) - 1
        return True

def cli_coordinates_input() -> tuple:
    while True:
        x = int(input("Please enter a x co-ordinate "))
        y = int(input("Please enter a y co-ordinate "))
        if  x > len(board) - 1 or y > len(board) - 1 or x < 0 or y < 0:
            print("Please enter a value between (inclusive) 0 and", len(board) - 1)
        else:
            break
    #Flipped due to the formatting nature of a list of lists. The first index is the row (y axis) and the second the column (x axis)
    return (y, x)

def simple_game_loop():
    print("Welcome to Battleships")
    global board
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
        
        