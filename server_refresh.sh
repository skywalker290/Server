cd /home/ubuntu/Server/
git pull 
sudo systemctl stop myapp
sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp