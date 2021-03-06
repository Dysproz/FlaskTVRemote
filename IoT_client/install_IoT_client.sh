#!/bin/sh

# Installation of required apt packages
cat apt-requirements.txt | xargs sudo apt install -y
if [ $? -ne 0 ]; then
	echo "Could not install required packages. Please check your packages. Exitting..."
	exit 1
fi

# Installation of required pip packages
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
	echo "Could not install required pip packages. Exitting..."
	exit 1
fi

# Setup of application files with respect to previous versions
sudo mkdir /var/lib/teleserver_IoT
sudo rm -rf /var/lib/teleserver_IoT/app > /dev/null
sudo chmod -R 777 /var/lib/teleserver_IoT/
sudo cp -rf $PWD /var/lib/teleserver_IoT/app/
sudo chmod -R +x /var/lib/teleserver_IoT/app
touch /var/lib/teleserver_IoT/data.yml

# Enable port 8080 in firewall
sudo ufw allow 8080

# Adding teleserver trigger to user profile
if [ $(grep -o "teleserver_IoT" ~/.profile | wc -l) = 0 ]; then
	echo "nohup python3 /var/lib/teleserver_IoT/app/IoT_run.py &" >> ~/.bashrc
fi

/var/lib/teleserver_IoT/app/tools/secret_manager.py

echo "Teleserver IoT client has been installed successfully. Now, restart your session to enjoy IoT client."
exit 0
