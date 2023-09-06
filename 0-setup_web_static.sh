#!/usr/bin/env bash
# set up web server for deployment

if ! [ -x "$(command -v nginx)" ]; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared/

echo "<html><body>Hello, web_static!</body></html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test /data/web_static/current

sudo chown -R ubuntu:ubuntu /data
sudo chmod -R 755 /data

sudo sed -i "s|location / {|location /hbnb_static/ {|" /etc/nginx/sites-available/default
sudo sed -i "s|alias /data/|alias /data/web_static/current/|" /etc/nginx/sites-available/default

sudo service nginx restart
