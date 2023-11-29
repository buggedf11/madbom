from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/clock')
def clock():
    return render_template('clock.html')

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/date')
def date():
    return render_template('Date.html')

@app.route('/other')
def other():
    return render_template('other.html')

if __name__ == '__main__':
    app.run(debug=False)
