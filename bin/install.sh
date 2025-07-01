#!/bin/bash

for cmd in git python3; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ '$cmd' is required but not installed. Please install it first."
        exit 1
    fi
done



echo "🤖 Welcome to your Terminal Assistant Installer!"
read -p "📝 What would you like to name your assistant command? (e.g., zeus, luna): " assistant

# Normalize name
assistant=$(echo "$assistant" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

INSTALL_DIR="$HOME/.${assistant}_cli"
REPO_URL="https://github.com/Lokeshsk29/shellpilot.git"
LAUNCHER="/usr/local/bin/$assistant"

# Clone repo
echo "📥 Cloning to $INSTALL_DIR ..."
git clone "$REPO_URL" "$INSTALL_DIR" || {
    echo "❌ Failed to clone repo."; exit 1;
}

# Save assistant name
echo "$assistant" > "$INSTALL_DIR/assistant_name.txt"

# Create launcher script
echo "#!/bin/bash
python3 \"$INSTALL_DIR/shellpilot/cli.py\" \"\$@\"" | sudo tee "$LAUNCHER" > /dev/null
sudo chmod +x "$LAUNCHER"

# Enable startup greeting by default
touch "$HOME/.shellpilot_enabled"

# Add to .bashrc or .zshrc
GREETER="python3 $INSTALL_DIR/shellpilot/startup_greet.py"
ADDED_LINE=false

if [ -f "$HOME/.bashrc" ]; then
    if ! grep -Fq "$GREETER" "$HOME/.bashrc"; then
        echo "" >> "$HOME/.bashrc"
        echo "# ShellPilot Greeting" >> "$HOME/.bashrc"
        echo "$GREETER" >> "$HOME/.bashrc"
        ADDED_LINE=true
    fi
fi

if [ -f "$HOME/.zshrc" ]; then
    if ! grep -Fq "$GREETER" "$HOME/.zshrc"; then
        echo "" >> "$HOME/.zshrc"
        echo "# ShellPilot Greeting" >> "$HOME/.zshrc"
        echo "$GREETER" >> "$HOME/.zshrc"
        ADDED_LINE=true
    fi
fi

echo "✅ Installed as command: $assistant"
echo "👉 Try running: $assistant hello"
if [ "$ADDED_LINE" = true ]; then
    echo "🧠 Assistant will greet you next time you open a terminal."
fi
