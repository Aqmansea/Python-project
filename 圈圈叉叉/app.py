from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

# 初始遊戲狀態
game_state = {
    "board": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
    "current_player": "X",
    "game_active": True,
    "winner": None
}

def check_winner(board):
    # 檢查勝利條件
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # 橫排
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # 直列
        [0, 4, 8], [2, 4, 6]             # 對角線
    ]
    for condition in win_conditions:
        if board[condition[0]] == board[condition[1]] == board[condition[2]] and board[condition[0]] != ' ':
            return board[condition[0]]
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/move', methods=['POST'])
def move():
    global game_state
    data = request.json
    index = data.get("index")
    
    # 確認遊戲是否在進行中並且該位置是空的
    if game_state["game_active"] and game_state["board"][index] == ' ':
        game_state["board"][index] = game_state["current_player"]
        winner = check_winner(game_state["board"])
        
        # 檢查是否有贏家
        if winner:
            game_state["game_active"] = False
            game_state["winner"] = winner
        elif ' ' not in game_state["board"]:  # 平局情況
            game_state["game_active"] = False
        else:
            # 交替玩家
            game_state["current_player"] = "O" if game_state["current_player"] == "X" else "X"
    
    return jsonify(game_state)

@app.route('/reset', methods=['POST'])
def reset():
    global game_state
    game_state = {
        "board": [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
        "current_player": "X",
        "game_active": True,
        "winner": None
    }
    return jsonify(game_state)

if __name__ == '__main__':
    app.run(debug=True)
