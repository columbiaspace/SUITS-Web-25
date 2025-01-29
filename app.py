from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime
from utils.discord_logger import DiscordLogger
from utils.llm_utils import get_llm_completion
from dotenv import load_dotenv
import os

app = Flask(__name__)
discord_logger = DiscordLogger()
load_dotenv()

discord_logger.send_log("Application starting up...", "info")

# Mock data generators
def generate_mock_vitals():
    discord_logger.send_log("Generating mock vitals data", "debug")
    vitals = {
        'heart_rate': random.randint(60, 100),
        'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 90)}",
        'o2_saturation': random.randint(95, 100),
        'suit_pressure': round(random.uniform(3.8, 4.2), 2),
        'battery_level': random.randint(70, 100),
        'co2_level': round(random.uniform(0, 2), 2)
    }
    discord_logger.send_log(f"Generated vitals: {vitals}", "debug")
    return vitals

def generate_mock_location():
    discord_logger.send_log("Generating mock location data", "debug")
    location = {
        'latitude': 29.5584 + random.uniform(-0.001, 0.001),  # JSC coordinates
        'longitude': -95.0930 + random.uniform(-0.001, 0.001),
        'heading': random.randint(0, 359)
    }
    discord_logger.send_log(f"Generated location: {location}", "debug")
    return location

# Routes
@app.route('/')
def index():
    discord_logger.send_log('Homepage accessed', "info")
    return render_template('index.html')

@app.route('/chat')
def chat():
    discord_logger.send_log('Chat interface accessed', "info")
    return render_template('chat.html')

@app.route('/verify-password', methods=['POST'])
def verify_password():
    data = request.get_json()
    if data.get('password') == os.getenv('CHAT_PASSWORD'):
        discord_logger.send_log('Successful chat login attempt', "info")
        return jsonify({'success': True}), 200
    discord_logger.send_log('Failed chat login attempt', "warning")
    return jsonify({'success': False}), 401

@app.route('/vitals')
def vitals():
    discord_logger.send_log('Vitals page accessed', "info")
    return render_template('vitals.html')

@app.route('/navigation')
def navigation():
    discord_logger.send_log('Navigation page accessed', "info")
    return render_template('navigation.html')

@app.route('/procedures')
def procedures():
    discord_logger.send_log('Procedures page accessed', "info")
    return render_template('procedures.html')

@app.route('/geology')
def geology():
    discord_logger.send_log('Geology page accessed', "info")
    return render_template('geology.html')

@app.route('/alerts')
def alerts():
    discord_logger.send_log('Alerts page accessed', "info")
    return render_template('alerts.html')

@app.route('/timeline')
def timeline():
    discord_logger.send_log('Timeline page accessed', "info")
    return render_template('timeline.html')

# API endpoints
@app.route('/api/vitals')
def get_vitals():
    discord_logger.send_log('Vitals data requested', "info")
    try:
        vitals = generate_mock_vitals()
        return jsonify(vitals)
    except Exception as e:
        error_msg = f"Error generating vitals data: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return jsonify({"error": error_msg}), 500

@app.route('/api/location')
def get_location():
    discord_logger.send_log('Location data requested', "info")
    try:
        location = generate_mock_location()
        return jsonify(location)
    except Exception as e:
        error_msg = f"Error generating location data: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return jsonify({"error": error_msg}), 500

# Remove all socket events and replace with HTTP endpoint
@app.route('/api/chat', methods=['POST'])
def chat_message():
    try:
        data = request.get_json()
        message = data['message']
        model = data.get('model', 'gpt-4o')
        messages = data.get('messages', [{'role': 'user', 'content': message}])
        
        discord_logger.send_log(f'Processing chat message with model {model}', "info")
        
        success, response = get_llm_completion(messages, model=model)
        if success:
            discord_logger.send_log('Successfully generated AI response', "info")
            return jsonify({'response': response})
        else:
            error_msg = f"Failed to generate AI response: {response}"
            discord_logger.send_log(error_msg, "error")
            return jsonify({'response': "Sorry, I encountered an error processing your request."}), 500
    except Exception as e:
        error_msg = f"Error in chat message handling: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return jsonify({'response': "An unexpected error occurred."}), 500

if __name__ == '__main__':
    try:
        discord_logger.send_log("Testing Discord connection...", "info")
        discord_logger.test_connection()
        discord_logger.send_log("Starting web server...", "info")
        app.run(host='0.0.0.0', port=80)
    except Exception as e:
        discord_logger.send_log(f"Critical error starting server: {str(e)}", "error") 
