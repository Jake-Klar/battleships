"""Module providing functions for flask server and multiplayer game functions"""
from flask import Flask, render_template, jsonify, request
import components
import mp_game_engine
#Will store all previous guesses to stop the AI from selecting the same co ordinated for no reason
previous_ai_guesses_flask = []
previous_user_guesses_flask = []
ai_board = []
ai_ships = {}
player_board = []
player_ships = {}
BOARD_SIZE = mp_game_engine.SIZE

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root() -> str:
    """Creates AI game components and displays primary game screen"""
    global ai_board, ai_ships
    ai_ships = components.create_battleships()
    ai_board = components.place_battleships(components.initialise_board(BOARD_SIZE), components.create_battleships(), 'random')
    return render_template('main.html', player_board=player_board)

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    """Creates user game components and siplays the placement game screen"""
    global player_ships
    player_ships = components.create_battleships()
    if request.method == 'GET':
        return render_template('placement.html', ships=player_ships, board_size=BOARD_SIZE)
    elif request.method == 'POST':
        data = request.get_json()
        global player_board
        player_board = components.place_battleships_flask(components.initialise_board(BOARD_SIZE), player_ships, data)
        return jsonify({"message": "Success"}), 200

@app.route('/attack', methods=['GET', 'POST'])
def attack() -> dict:
    """Handles attacks for both players Ends the gmae when one's navy is destroyed"""
    if request.args:
        while True:
            x = int(request.args.get('x'))
            y = int(request.args.get('y'))
            if (y, x) not in previous_user_guesses_flask:
                previous_user_guesses_flask.append((y, x))
                break
        #Flipped due to the formatting nature of a list of lists.
        if mp_game_engine.attack((y, x), ai_board, ai_ships) is True:
            for name, count in ai_ships.items():
                if count == 0:
                    ai_ships.pop(name)
                    break
            if len(ai_ships) == 0:
                return {"hit": True, "AI_Turn": mp_game_engine.generate_attack_flask(previous_ai_guesses_flask), "finished": "The player has won the game"}
            else:
                location = mp_game_engine.generate_attack_flask(previous_ai_guesses_flask)
                previous_ai_guesses_flask.append(location)
                mp_game_engine.attack(location, player_board, player_ships)
                for name, count in player_ships.items():
                    if count == 0:
                        player_ships.pop(name)
                        break
                if len(player_ships) == 0:
                    return {"hit": True, "AI_Turn": location, "finished": "The AI has won the game"}
                else:
                    return {"hit": True, "AI_Turn": location}
        else:
            location = mp_game_engine.generate_attack_flask(previous_ai_guesses_flask)
            previous_ai_guesses_flask.append(location)
            mp_game_engine.attack(location, player_board, player_ships)
            for name, count in player_ships.items():
                if count == 0:
                    player_ships.pop(name)
                    break
            if len(player_ships) == 0:
                return {"hit": False, "AI_Turn": location, "finished": "The AI has won the game"}
            else:
                return {"hit": False, "AI_Turn": location}
if __name__ == '__main__':
    app.template_folder = "templates"
    app.run()
