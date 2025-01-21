from flask import Flask, render_template, jsonify, request
import json
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.update(
    UPLOAD_FOLDER='static/downloads',
    SQLALCHEMY_DATABASE_URI='sqlite:///test.db'
)
db = SQLAlchemy(app)

class User(db.Model):
    """User model for database."""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    money = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

def load_json_file(filepath):
    """Helper function to load JSON files."""
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return None
    
def save_json_file(filepath, data):
    """Helper function to save JSON files."""
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/save_users', methods=['POST'])
def save_users():
    """Save user data to JSON file."""
    users = request.json
    save_json_file('static/users.json', users)
    return jsonify({'success': 'Users saved successfully'}), 200

@app.route('/getMaxBet', methods=['GET'])
def get_max_bet():
    """Get maximum bet for a specific game."""
    game = request.args.get('game')
    config = load_json_file('static/config.json')
    
    if not config:
        return jsonify({'error': 'Config file not found'}), 500
    
    max_bet = config['games'].get(game, {}).get('maxBet')
    if max_bet is None:
        return jsonify({'error': 'Game not found or maxBet not set'}), 404
        
    return jsonify({'maxBet': max_bet}), 200

@app.route('/updateBetLimits', methods=['POST'])
def update_bet_limits():
    """Update betting limits for games."""
    bet_limits = request.json.get('games')
    if bet_limits is None:
        return jsonify({'error': 'Invalid data'}), 400

    try:
        data = load_json_file('static/admin/max_bet_limits.json')
        if data is None:
            return jsonify({'error': 'Bet limits file not found'}), 500
        
        data['games'] = bet_limits
        save_json_file('static/admin/max_bet_limits.json', data)
        return jsonify({'message': 'Bet limits updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/updateUser', methods=['POST'])
def update_user():
    """Update user information including inventory."""
    try:
        data = request.get_json()
        if not isinstance(data, list):
            # Handle single user update
            if not isinstance(data, dict):
                return jsonify({'error': 'Invalid data format'}), 400
            data = [data]

        users = load_json_file('static/users.json')
        if users is None:
            return jsonify({'error': 'User data file not found'}), 500

        updated_users = []
        for item in data:
            username = item.get('username')
            money = item.get('money')
            inventory = item.get('inventory')

            if not username or not isinstance(money, (int, float)):
                return jsonify({'error': 'Invalid user data: username must be string and money must be number'}), 400

            user = next((u for u in users if u['username'] == username), None)
            if not user:
                return jsonify({'error': f'User {username} not found'}), 404

            user['money'] = money
            if inventory is not None:
                user['inventory'] = inventory
            updated_users.append(user)

        save_json_file('static/users.json', users)
        return jsonify({'success': True, 'updatedUsers': updated_users}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=3000, debug=False)