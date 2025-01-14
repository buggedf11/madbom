from flask import Flask, render_template, jsonify, send_from_directory, request
import os

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

@app.route('/downloads.html')
def downloads():
    return render_template('downloads.html')

@app.route('/api/files')
def list_files():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    return jsonify(files)

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file:
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        return jsonify({'success': 'File uploaded successfully'}), 200

if __name__ == '__main__':
    app.run(debug=True)