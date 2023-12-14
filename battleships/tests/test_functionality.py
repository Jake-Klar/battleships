from components import initialise_board, create_battleships, place_battleships
from game_engine import attack
import os


def test_initialise_board_return_size():
    """
    Test if the initialise_board function returns a list of the correct size.
    """
    size = 10
    # Run the function
    board = initialise_board(size)
    # Check that the return is a list
    assert isinstance(board, list), "initialise_board function does not return a list"
    # check that the length of the list is the same as board
    assert len(board) == size, "initialise_board function does not return a list of the correct size"
    for row in board:
        # Check that each sub element is a list
        assert isinstance(row, list), "initialise_board function does not return a list of lists"
        # Check that each sub list is the same size as board
        assert len(row) == size, "initialise_board function does not return lists of the correct size"

def test_create_battleships_return_size():
    """
    Test if the create_battleships function returns a dictionary of the correct size
    """
    file = 'battleships.txt'
    #Run the function
    ships = create_battleships(file)
    #Find the amount of ships there should be
    path = os.getcwd() + '\\' + file
    f = open(path, 'r')
    lines = f.readlines()
    length = len(lines)
    #Check that the return is a dictionary
    assert isinstance(ships, dict), "create_battleships function does not return a dictionary"
    #Check the amount of the ships is the same as the length of the battleships.txt length
    assert len(ships) == length, "create_battleships function does not return a dictionary of the correct size"

def test_place_battleships_amount():
    """
    Test if the place_battleships function places the correct number of ships onto the board
    """
    file = 'battleships.txt'
    board = initialise_board()
    ships = create_battleships(file)
    #Find the amount of ships ther eshould be
    num = sum(ships.values())
    #Run the function
    place_battleships(board, ships)
    ship_amount = 0
    for row in board:
        for cell in row:
            if cell is not None:
                ship_amount += 1
    #Check that the amount of ships on the board is equal to the total length of all ships in the file
    assert num == ship_amount, "place_battleships function does not place the correct number of ships"

def test_attack_returns_correct():
    """
    Test if the attack function returns the correct bool
    """
    #Initialize a board with a predermined ship at 0, 0 and a tuple of (0, 0)
    board = [['ship']]
    ships = {'ship': 1}
    coords = (0, 0)
    #Run the function
    response = attack(coords, board, ships)
    #Check a bool is returned
    assert isinstance(response, bool), "attack does not return a bool"
    #Check if the correct bool is returned
    assert response is True, "attack does not return the correct bool"