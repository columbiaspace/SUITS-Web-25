from flask import Flask, render_template, jsonify, request
import json
import random
from datetime import datetime, timedelta
from utils.discord_logger import DiscordLogger
from utils.llm_utils import get_llm_completion
from dotenv import load_dotenv
import os

app = Flask(__name__)
discord_logger = DiscordLogger()
load_dotenv()

# Configure Jinja2
app.jinja_env.filters['tojson'] = json.dumps
app.jinja_env.trim_blocks = True
app.jinja_env.lstrip_blocks = True

# Add custom filters
@app.template_filter('lower')
def lower_filter(s):
    return str(s).lower()

@app.template_filter('round')
def round_filter(value):
    return round(float(value))

discord_logger.send_log("Application starting up...", "info")

# Enhanced Mock data generators
def generate_mock_vitals():
    discord_logger.send_log("Generating mock vitals data", "debug")
    vitals = {
        'heart_rate': random.randint(60, 100),
        'blood_pressure': f"{random.randint(110, 130)}/{random.randint(70, 90)}",
        'o2_saturation': random.randint(95, 100),
        'suit_pressure': round(random.uniform(3.8, 4.2), 2),
        'battery_level': random.randint(70, 100),
        'co2_level': round(random.uniform(0, 2), 2),
        'temperature': round(random.uniform(98.0, 99.5), 1),
        'humidity': random.randint(40, 60),
        'fan_speed': random.randint(2000, 3000),
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    discord_logger.send_log(f"Generated vitals: {vitals}", "debug")
    return vitals

def generate_mock_location():
    discord_logger.send_log("Generating mock location data", "debug")
    location = {
        'latitude': 29.5584 + random.uniform(-0.001, 0.001),
        'longitude': -95.0930 + random.uniform(-0.001, 0.001),
        'heading': random.randint(0, 359),
        'altitude': round(random.uniform(0, 10), 2),
        'speed': round(random.uniform(0, 2), 2),
        'waypoints': [
            {'name': 'Base Camp', 'lat': 29.5584, 'lng': -95.0930},
            {'name': 'Collection Site A', 'lat': 29.5590, 'lng': -95.0935},
            {'name': 'Collection Site B', 'lat': 29.5580, 'lng': -95.0925}
        ],
        'last_updated': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    discord_logger.send_log(f"Generated location: {location}", "debug")
    return location

def generate_mock_procedures():
    procedures = {
        'current_procedure': {
            'name': 'Sample Collection Protocol',
            'step': 3,
            'total_steps': 8,
            'time_remaining': '45:00',
            'status': 'In Progress'
        },
        'completed_procedures': [
            {'name': 'Equipment Check', 'duration': '15:00', 'status': 'Completed'},
            {'name': 'Communication Test', 'duration': '10:00', 'status': 'Completed'}
        ],
        'upcoming_procedures': [
            {'name': 'Site Documentation', 'estimated_duration': '30:00', 'priority': 'High'},
            {'name': 'Sample Storage', 'estimated_duration': '20:00', 'priority': 'Medium'}
        ]
    }
    return procedures

def generate_mock_geology_data():
    geology_data = {
        'current_sample': {
            'id': f'SAMPLE-{random.randint(100, 999)}',
            'type': random.choice(['Basalt', 'Breccia', 'Regolith']),
            'mass': round(random.uniform(0.1, 2.0), 2),
            'location': {'lat': 29.5584, 'lng': -95.0930},
            'collection_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        'collected_samples': [
            {'id': 'SAMPLE-101', 'type': 'Basalt', 'status': 'Analyzed'},
            {'id': 'SAMPLE-102', 'type': 'Regolith', 'status': 'Stored'},
            {'id': 'SAMPLE-103', 'type': 'Breccia', 'status': 'In Analysis'}
        ],
        'equipment_status': {
            'xrf_device': 'Operational',
            'sample_bags': 15,
            'collection_tools': 'All Available'
        }
    }
    return geology_data

def generate_mock_alerts():
    alerts = {
        'critical': [
            {'type': 'Battery', 'message': 'Battery level below 25%', 'timestamp': (datetime.now() - timedelta(minutes=5)).strftime("%Y-%m-%d %H:%M:%S")} if random.random() < 0.2 else None
        ],
        'warnings': [
            {'type': 'O2', 'message': 'O2 level trending downward', 'timestamp': (datetime.now() - timedelta(minutes=15)).strftime("%Y-%m-%d %H:%M:%S")} if random.random() < 0.3 else None
        ],
        'notifications': [
            {'type': 'Schedule', 'message': 'Next procedure in 10 minutes', 'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
        ]
    }
    return {k: [v for v in vs if v is not None] for k, vs in alerts.items()}

def generate_mock_timeline():
    current_time = datetime.now()
    timeline = {
        'mission_time': '02:30:00',
        'events': [
            {
                'time': (current_time - timedelta(minutes=30)).strftime("%H:%M"),
                'event': 'Started EVA',
                'status': 'Completed'
            },
            {
                'time': (current_time + timedelta(minutes=30)).strftime("%H:%M"),
                'event': 'Sample Collection',
                'status': 'Upcoming'
            },
            {
                'time': (current_time + timedelta(hours=1)).strftime("%H:%M"),
                'event': 'Return to Base',
                'status': 'Scheduled'
            }
        ],
        'remaining_time': '01:30:00'
    }
    return timeline

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
    return render_template('vitals.html', vitals_data=generate_mock_vitals())

@app.route('/navigation')
def navigation():
    discord_logger.send_log('Navigation page accessed', "info")
    return render_template('navigation.html', location_data=generate_mock_location())

@app.route('/procedures')
def procedures():
    try:
        discord_logger.send_log('Procedures page accessed', "info")
        procedures_data = generate_mock_procedures()
        discord_logger.send_log(f'Generated procedures data: {procedures_data}', "debug")
        return render_template('procedures.html', procedures_data=procedures_data)
    except Exception as e:
        error_msg = f"Error in procedures route: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return render_template('error.html', error=error_msg), 500

@app.route('/geology')
def geology():
    try:
        discord_logger.send_log('Geology page accessed', "info")
        geology_data = generate_mock_geology_data()
        discord_logger.send_log(f'Generated geology data: {geology_data}', "debug")
        return render_template('geology.html', geology_data=geology_data)
    except Exception as e:
        error_msg = f"Error in geology route: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return render_template('error.html', error=error_msg), 500

@app.route('/alerts')
def alerts():
    discord_logger.send_log('Alerts page accessed', "info")
    return render_template('alerts.html', alerts_data=generate_mock_alerts())

@app.route('/timeline')
def timeline():
    try:
        discord_logger.send_log('Timeline page accessed', "info")
        timeline_data = generate_mock_timeline()
        discord_logger.send_log(f'Generated timeline data: {timeline_data}', "debug")
        return render_template('timeline.html', timeline_data=timeline_data)
    except Exception as e:
        error_msg = f"Error in timeline route: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return render_template('error.html', error=error_msg), 500

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

@app.route('/api/procedures')
def get_procedures():
    discord_logger.send_log('Procedures data requested', "info")
    try:
        procedures = generate_mock_procedures()
        return jsonify(procedures)
    except Exception as e:
        error_msg = f"Error generating procedures data: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return jsonify({"error": error_msg}), 500

@app.route('/api/geology')
def get_geology():
    discord_logger.send_log('Geology data requested', "info")
    try:
        geology = generate_mock_geology_data()
        return jsonify(geology)
    except Exception as e:
        error_msg = f"Error generating geology data: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return jsonify({"error": error_msg}), 500

@app.route('/api/alerts')
def get_alerts():
    discord_logger.send_log('Alerts data requested', "info")
    try:
        alerts = generate_mock_alerts()
        return jsonify(alerts)
    except Exception as e:
        error_msg = f"Error generating alerts data: {str(e)}"
        discord_logger.send_log(error_msg, "error")
        return jsonify({"error": error_msg}), 500

@app.route('/api/timeline')
def get_timeline():
    discord_logger.send_log('Timeline data requested', "info")
    try:
        timeline = generate_mock_timeline()
        return jsonify(timeline)
    except Exception as e:
        error_msg = f"Error generating timeline data: {str(e)}"
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
