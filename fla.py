from flask import Flask, render_template, jsonify, send_from_directory
import os

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

@app.route('/sound.html')
def sound():
    return render_template('sound.html')

@app.route('/downloads.html')
def downloads():
    return render_template('downloads.html')

@app.route('/api/files')
def list_files():
    files = os.listdir('static/downloads')  # Ensure this path is correct
    return jsonify(files)

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory('static/downloads', filename)  # Ensure this path is correct

if __name__ == '__main__':
    app.run(debug=True)