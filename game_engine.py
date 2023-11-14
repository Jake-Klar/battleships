import components

def attack(coordinates: tuple, board: list, ships: dict) -> bool:
    if board[coordinates[0]][coordinates[1]] == None:
        return False
    else:
        ships[board[coordinates[0]][coordinates[1]]] = int(ships[board[coordinates[0]][coordinates[1]]]) - 1
        print(ships[board[coordinates[0]][coordinates[1]]])
        return True

def cli_coordinates_input() -> tuple:
    x = int(input("Please enter a x co-ordinate "))
    y = int(input("Please enter a y co-ordinate "))
    return (x, y)

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
        if attack(coordinates, board, ships) == True:
            board[coordinates[0]][coordinates[1]] = None
            print("Hit")
            for name, count in ships.items():
                if count == 0:
                    print(name, "has been sunk")
                    ships.pop(name)
                    break  
        else:
            print("Miss")
        
        