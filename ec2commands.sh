# Install dependencies
sudo apt update
sudo apt install python3-pip python3-dev nginx
pip install gunicorn

# Copy configs
sudo cp config/nginx.conf /etc/nginx/sites-available/lunarapp
sudo ln -s /etc/nginx/sites-available/lunarapp /etc/nginx/sites-enabled/
sudo cp config/lunarapp.service /etc/systemd/system/

# Start services
sudo systemctl daemon-reload
sudo systemctl start lunarapp
sudo systemctl enable lunarapp
sudo systemctl restart nginx