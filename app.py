from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO
import json
import random
from datetime import datetime
from utils.discord_logger import DiscordLogger

app = Flask(__name__)
socketio = SocketIO(app)
discord_logger = DiscordLogger()

# Mock data generators
def generate_mock_vitals():
    return {
        'heart_rate': random.randint(60, 100),
        'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 90)}",
        'o2_saturation': random.randint(95, 100),
        'suit_pressure': round(random.uniform(3.8, 4.2), 2),
        'battery_level': random.randint(70, 100),
        'co2_level': round(random.uniform(0, 2), 2)
    }

def generate_mock_location():
    return {
        'latitude': 29.5584 + random.uniform(-0.001, 0.001),  # JSC coordinates
        'longitude': -95.0930 + random.uniform(-0.001, 0.001),
        'heading': random.randint(0, 359)
    }

# Routes
@app.route('/')
def index():
    discord_logger.send_log('New client connected')
    return render_template('index.html')

@app.route('/vitals')
def vitals():
    discord_logger.send_log('Vitals page accessed')
    return render_template('vitals.html')

@app.route('/navigation')
def navigation():
    return render_template('navigation.html')

@app.route('/procedures')
def procedures():
    return render_template('procedures.html')

@app.route('/geology')
def geology():
    return render_template('geology.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')

@app.route('/timeline')
def timeline():
    return render_template('timeline.html')

# API endpoints
@app.route('/api/vitals')
def get_vitals():
    return jsonify(generate_mock_vitals())

@app.route('/api/location')
def get_location():
    return jsonify(generate_mock_location())

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    discord_logger.send_log('New client connected')

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')
    discord_logger.send_log('Client disconnected')

if __name__ == '__main__':
    discord_logger.test_connection()
    socketio.run(app, 
                    host='0.0.0.0',  # Listen on all interfaces
                    port=80,       # Specify port
                    )     # Disable debug mode in production 