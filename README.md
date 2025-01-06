# Lunar Lions Web Application

## EC2 Deployment Instructions

1. Clone the repository on your EC2 instance:
```bash
git clone <your-repo-url>
cd LunarLionsWeb
```

2. Set up a Python virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3. Set up the systemd service:
```bash
sudo cp lunar-lions.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable lunar-lions
sudo systemctl start lunar-lions
```

4. Check the service status:
```bash
sudo systemctl status lunar-lions
```

5. The application will be running on port 8000. Make sure to:
   - Configure your EC2 security group to allow inbound traffic on port 8000
   - Use your EC2's public IP or domain name to access the application

## Logs
- Application logs: /home/ubuntu/LunarLionsWeb/gunicorn-*.log
- System service logs: `sudo journalctl -u lunar-lions`