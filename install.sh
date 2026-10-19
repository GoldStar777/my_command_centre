#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_LABEL="com.$USER.commandcentre"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"

echo "=== Command Centre Setup ==="

# 1. Ask user for their preferred display name
read -p "Enter your name for the app (press Enter for 'My'): " USER_INPUT_NAME
if [ -z "$USER_INPUT_NAME" ]; then
    DISPLAY_NAME="My Command Centre"
else
    DISPLAY_NAME="${USER_INPUT_NAME}'s Command Centre"
fi

# Save the chosen name into a local config file
echo "APP_DISPLAY_NAME=\"${DISPLAY_NAME}\"" > "$APP_DIR/.config.env"
echo "Configured app as: $DISPLAY_NAME"

# 2. Virtual environment setup
if [ ! -d "$APP_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$APP_DIR/.venv"
fi

echo "Installing dependencies..."
"$APP_DIR/.venv/bin/pip" install --quiet -r "$APP_DIR/requirements.txt"

# 3. Safely reload the launchd service
echo "Registering background service..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true

cat <<EOF > "$PLIST_PATH"
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_LABEL}</string>
    <key>ProgramArguments</key>
    <array>
        <string>${APP_DIR}/.venv/bin/python</string>
        <string>${APP_DIR}/app.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>${APP_DIR}</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>${APP_DIR}/commandcentre.log</string>
    <key>StandardErrorPath</key>
    <string>${APP_DIR}/commandcentre_err.log</string>
</dict>
</plist>
EOF

launchctl load "$PLIST_PATH"

echo ""
echo " Setup complete! App is running in the background."
echo "1. Open Safari and go to: http://localhost:8000"
echo "2. Click: File -> Add to Dock"
echo "3. It will default to: '$DISPLAY_NAME'"
