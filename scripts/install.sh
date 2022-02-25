#!/bin/bash
# Check if script is running as root or not.
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Check if installer is running from a cloned repo or not.
AUX_FILE=.gitkeep
if test -f "$AUX_FILE"; then
    cd ..
else
    git clone https://github.com/sammwyy/meowshot
    cd meowshot
fi

# Install dependencies.
sudo apt-get install python3-tk python3-dev scrot

# Install python dependencies.
pip install -r requirements.txt > /dev/null

# Move source files to /usr/share.
sudo mkdir /usr/share/meowshot
sudo cp -r ./src/* /usr/share/meowshot

# Create bin under /usr/bin.
echo "#!/bin/bash" > /usr/bin/meowshot
echo "python /usr/share/meowshot/main.py" >> /usr/bin/meowshot
sudo chmod 755 /usr/bin/meowshot

# Start
echo "Installed"
exit