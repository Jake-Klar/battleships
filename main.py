from flask import Flask, render_template, jsonify, request
import components
import mp_game_engine

app = Flask(__name__)

@app.route('/', methods=['GET'])
def root():
    global ai_board, ai_ships
    ai_ships = components.create_battleships()
    ai_board = components.place_battleships(components.initialise_board(), components.create_battleships(), None, 'random')
    for i in ai_board:
        print(i)
    return render_template('main.html', player_board=player_board)

@app.route('/placement', methods=['GET', 'POST'])
def placement_interface():
    global player_ships
    player_ships = components.create_battleships()
    board_size = 10
    if request.method == 'GET':
        return render_template('placement.html', ships=player_ships, board_size=board_size)
    elif request.method == 'POST':
        data = request.get_json()
        global player_board
        player_board = components.place_battleships(components.initialise_board(), player_ships, data, 'web')
        return jsonify({"message": "Success"}), 200

@app.route('/attack', methods=['GET', 'POST'])
def attack():
    if request.args:
        x = int(request.args.get('x'))
        y = int(request.args.get('y'))
        #Flipped due to the formatting nature of a list of lists. The first index is the row (y axis) and the second the column (x axis)
        location = ai_board[y][x]
        if mp_game_engine.attack(location, ai_ships) == True:
            for name, count in ai_ships.items():
                if count == 0:
                    ai_ships.pop(name)
                    break
            if len(ai_ships) == 0:
                return {"hit": True, "AI_Turn": mp_game_engine.generate_attack(), "finished": "The player has won the game"}
            else:
                return {"hit": True, "AI_Turn": mp_game_engine.generate_attack()}
        else:
            return {"hit": False, "AI_Turn": mp_game_engine.generate_attack()}
        
        
if __name__ == '__main__':
    app.template_folder = "templates"
    app.run()