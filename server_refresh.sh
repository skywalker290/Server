git pull /home/ubuntu/Server/.
sudo systemctl stop myapp
sudo systemctl daemon-reload
sudo systemctl start myapp
sudo systemctl enable myapp