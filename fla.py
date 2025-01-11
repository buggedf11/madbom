from flask import Flask, render_template, send_file

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/loggedin')
def loggedin():
    return render_template('loggedin.html')

@app.route('/user.json')
def user_json():
    return send_file('user.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)