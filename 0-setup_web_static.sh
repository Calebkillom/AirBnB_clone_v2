#!/usr/bin/env bash
# Bash script that sets up your web servers for the deployment of web_static

# installing Nginx if not installed
if ! dpkg -l | grep -q nginx; then
	sudo apt update
	sudo apt -y install nginx
	sudo ufw applist
	sudo ufw allow "Nginx HTTP"
fi

# creating the relevant/necessary directories if they do not exist
sudo mkdir -p /data/web_static/releases/test /data/web_static/shared

# Creating a Fake Html File
echo "<html><head></head><body>Holberton School</body></html>" | sudo tee /data/web_static/releases/test/index.html

# Creating symbolic link between two folders, deleting if it exists and recreating
if [ -L /data/web_static/current ]; then
    sudo rm /data/web_static/current
fi
sudo ln -s /data/web_static/releases/test /data/web_static/current

# Giving ownership of the /data/ folder to the ubuntu user AND group
sudo chown -R ubuntu:ubuntu /data/

# Updating the Nginx configuration to serve the  relevant contents
echo "server {
    listen 80;
    listen [::]:80 default_server;
    root   /etc/nginx/html;
    index  index.html index.htm;

		location /hbnb_static/ {
        alias /data/web_static/current/;
				index index.html;
    }

    # Redirecting any requests to /redirect_me to a YouTube video
    location /redirect_me {
        return 301 https://www.youtube.com/;
    }

    # Using a custom 404 error page
    error_page 404 /404.html;
    location = /404.html {
        root /etc/nginx/html;
        internal;
    }
	# Adding the header with server hostname
	add_header X-Served-By \$hostname;
}" | sudo tee /etc/nginx/sites-available/default > /dev/null

# Restarting the Nginx service to apply the changes
sudo service nginx restart
