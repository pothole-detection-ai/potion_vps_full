sudo apt upgrade -y
sudo apt update -y
sudo apt install nginx -y
sudo pip install -r /home/linuxuser/potion/requirements.txt
sudo systemctl enable nginx
sudo ufw allow 'Nginx Full'
sudo ufw allow 5000/tcp
sudo systemctl restart nginx

sudo ufw status
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx
