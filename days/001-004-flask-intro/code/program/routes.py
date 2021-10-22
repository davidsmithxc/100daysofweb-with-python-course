from datetime import datetime
from flask import render_template
from program import app
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Template Demo', time=datetime.now())

@app.route('/100Days')
def p100days():
    return render_template('100Days.html')

@app.route('/truck')
def truck_status():
    pidfile = "/tmp/truck.pid"
    if os.path.isfile(pidfile):
        with open(pidfile, 'r') as f:
            otherID = f.read()
        status = f'running with ID {otherID}'
    else:
        status = 'not running'
        os.system('/usr/bin/python3 /home/pi/truck/truck_mainRC.py')

    return render_template('truck.html', title='Truck Status', status=status)

@app.route('/secret')
def secret():
    return render_template('secret.html')
