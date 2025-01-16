from flask import Flask, render_template, jsonify, send_from_directory, request
import os
import json

app = Flask(__name__)
UPLOAD_FOLDER = 'static/downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/calendar.html')
def calendar():
    return render_template('calendar.html')

@app.route('/sound.html')
def sound():
    return render_template('sound.html')

@app.route('/bank.html')
def bank():
    return render_template('bank.html')

@app.route('/AdminPage.html')
def admin():
    return render_template('AdminPage.html')

@app.route('/blackj.html')
def blackjack():
    return render_template('blackj.html')

@app.route('/higherorlowwer.html')
def higherorlowwer():
    return render_template('higherorlowwer.html')

@app.route('/static/users.json')
def get_users():
    return send_from_directory('static', 'users.json')

@app.route('/roule.html')
def roule():
    return render_template("roule.html")

@app.route('/api/save_users', methods=['POST'])
def save_users():
    users = request.json
    with open('static/users.json', 'w') as f:
        json.dump(users, f)
    return jsonify({'success': 'Users saved successfully'}), 200

@app.route('/getMaxBet', methods=['GET'])
def get_max_bet():
    game = request.args.get('game')
    try:
        with open('static/config.json', 'r') as file:
            config = json.load(file)
        max_bet = config['games'].get(game, {}).get('maxBet')
        if max_bet is None:
            return jsonify({'error': 'Game not found or maxBet not set'}), 404
        return jsonify({'maxBet': max_bet}), 200
    except FileNotFoundError:
        return jsonify({'error': 'Config file not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/updateUser', methods=['POST'])
def update_user():
    data = request.get_json()
    username = data.get('username')
    money = data.get('money')

    try:
        with open('static/users.json', 'r') as file:
            users = json.load(file)
    except FileNotFoundError:
        return jsonify({'error': 'User data file not found'}), 500

    user_found = False
    for user in users:
        if user['username'] == username:
            user['money'] = money
            user_found = True
            break

    if not user_found:
        return jsonify({'error': 'User not found'}), 404

    try:
        with open('static/users.json', 'w') as file:
            json.dump(users, file, indent=2)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

    return jsonify({'success': 'User updated successfully'}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=False)