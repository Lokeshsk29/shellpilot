#!/bin/bash

echo "🤖 Welcome to your Terminal Assistant Installer!"
read -p "📝 What would you like to name your assistant command? (e.g., zeus, luna): " assistant

# Normalize name
assistant=$(echo "$assistant" | tr '[:upper:]' '[:lower:]' | tr -d ' ')

INSTALL_DIR="$HOME/.${assistant}_cli"
REPO_URL="https://github.com/Lokeshsk29/shellpilot.git"
LAUNCHER="/usr/local/bin/$assistant"

# Check dependencies
for cmd in git python3; do
    if ! command -v $cmd &> /dev/null; then
        echo "❌ Required command '$cmd' is not installed. Please install it and try again."
        exit 1
    fi
done

# Clone repo
echo "📥 Cloning to $INSTALL_DIR ..."
git clone "$REPO_URL" "$INSTALL_DIR" || {
    echo "❌ Failed to clone repo. Check internet connection or URL."; exit 1;
}

# Save assistant name
echo "$assistant" > "$INSTALL_DIR/assistant_name.txt"

# Install Python dependencies if requirements.txt exists
if [ -f "$INSTALL_DIR/requirements.txt" ]; then
    echo "📦 Installing Python dependencies..."
    python3 -m pip install --user -r "$INSTALL_DIR/requirements.txt" || {
        echo "⚠️ Warning: Some dependencies may not have installed."
    }
fi

# Create launcher script (needs sudo)
echo "🔧 Creating command: $assistant"
if ! echo "#!/bin/bash
python3 \"$INSTALL_DIR/shellpilot/cli.py\" \"\$@\"" | sudo tee "$LAUNCHER" > /dev/null; then
    echo "❌ Failed to create launcher command. You may have entered the wrong sudo password."
    echo "🛑 Installation aborted. Try again with the correct password."
    exit 1
fi

sudo chmod +x "$LAUNCHER"

# Enable startup greeting by default
touch "$HOME/.shellpilot_enabled"

# Add greeting to shell startup file
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

# Final success message
echo "✅ Installed as command: $assistant"
echo "👉 Try running: $assistant hello"
if [ "$ADDED_LINE" = true ]; then
    echo "🧠 Assistant will greet you next time you open a terminal."
fi
