#!/bin/bash
# Check if script is running as root or not.
if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

# Delete files.
sudo rm -rf /usr/share/meowshot

# Delete binary.
sudo rm -rf /usr/bin/meowshot

echo "Uninstalled."