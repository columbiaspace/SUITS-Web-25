import requests
import json
import os 
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

class DiscordLogger:
    def __init__(self):
        self.webhook_url = WEBHOOK_URL
        if not self.webhook_url:
            logging.warning("Discord webhook URL not found in environment variables")

    def send_log(self, message, level="INFO"):
        """
        Send a log message to Discord
        Args:
            message (str): The message to send
            level (str): Log level (INFO, WARNING, ERROR, etc.)
        """
        if not self.webhook_url:
            return
        
        try:
            payload = {
                "content": f"[{level}] {message}"
            }
            response = requests.post(self.webhook_url, json=payload)
            response.raise_for_status()
        except Exception as e:
            logging.error(f"Failed to send Discord log: {str(e)}")

    def test_connection(self):
        """Test the Discord webhook connection"""
        self.send_log("Test logging connection successful") 