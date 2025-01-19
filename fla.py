from flask import Flask, render_template, jsonify, send_from_directory, request
import json
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
UPLOAD_FOLDER = 'static/downloads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    money = db.Column(db.Float, default=0)

class InventoryItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_name = db.Column(db.String(120), nullable=False)
    item_rarity = db.Column(db.String(50), nullable=False)
    item_value = db.Column(db.Float, nullable=False)
    

@app.route('/')
def index():
    return render_template('index.html')



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

@app.route('/updateBetLimits', methods=['POST'])
def update_bet_limits():
    try:
        bet_limits = request.json.get('games')
        if bet_limits is None:
            return jsonify({'error': 'Invalid data'}), 400

        with open('static/admin/max_bet_limits.json', 'r+') as file:
            data = json.load(file)
            data['games'] = bet_limits
            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

        return jsonify({'message': 'Bet limits updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/updateUser', methods=['POST'])
def update_user():
    try:
        data = request.get_json()

        if not isinstance(data, list):
            return jsonify({'error': 'Invalid data format: Expected a list'}), 400

        with open('static/users.json', 'r') as file:
            users = json.load(file)

        updated_users = []
        for item in data:
            username = item.get('username')
            money = item.get('money')

            if not username or not isinstance(money, (int, float)):
                return jsonify({'error': 'Invalid user data: username must be string and money must be number'}), 400

            user_found = False
            for user in users:
                if user['username'] == username:
                    user['money'] = money
                    user_found = True
                    updated_users.append(user)
                    break

            if not user_found:
                return jsonify({'error': f'User {username} not found'}), 404

        with open('static/users.json', 'w') as file:
            json.dump(users, file, indent=2)

        return jsonify({'success': 'Users updated successfully', 'updatedUsers': updated_users}), 200

    except FileNotFoundError:
        return jsonify({'error': 'User data file not found'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=False)