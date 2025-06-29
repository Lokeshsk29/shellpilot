#!/bin/bash

echo " Welcome to your Terminal Assistant Installer!"
read -p "What would you like to name  your assistant  Name? (e.g., Zeus):" assistant

assistant = $(echo "$assistant" | tr '[:upper]' '[:lower]' | tr -d " ")

INSTALL_DIR = "$HOME/.${assistant}_cli"