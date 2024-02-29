from flask import render_template
from flask import Flask
import psutil
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

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
    cpu_percent = psutil.cpu_percent()
    memory_percent = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    network_stats = psutil.net_io_counters()
    network_bytes_sent = network_stats.bytes_sent
    network_bytes_received = network_stats.bytes_recv
    return render_template('other.html', cpu_percent=cpu_percent, memory_percent=memory_percent, disk_usage=disk_usage, network_bytes_sent=network_bytes_sent, network_bytes_received=network_bytes_received)

if __name__ == '__main__':
    app.run(debug=False)
