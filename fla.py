from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/main.html')
def main():
    return render_template('main.html')

@app.route('/calendar.html')
def calendar():
    return render_template('calendar.html')

if __name__ == '__main__':
    app.run(debug=True)