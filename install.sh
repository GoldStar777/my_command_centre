#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_LABEL="com.$USER.commandcentre"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"

echo "========================================"
echo "       Command Centre Setup (macOS)     "
echo "========================================"
echo ""

# 1. Ask for user name
read -p "Enter your name (press Enter for 'My'): " USER_INPUT_NAME
if [ -z "$USER_INPUT_NAME" ]; then
    PREFIX="My"
else
    PREFIX="${USER_INPUT_NAME}'s"
fi

# 2. Ask for custom app title
read -p "What do you want to call this app? (press Enter for 'Command Centre'): " USER_INPUT_TITLE
if [ -z "$USER_INPUT_TITLE" ]; then
    APP_TITLE="Command Centre"
else
    APP_TITLE="$USER_INPUT_TITLE"
fi

DISPLAY_NAME="${PREFIX} ${APP_TITLE}"
echo "APP_DISPLAY_NAME=\"${DISPLAY_NAME}\"" > "$APP_DIR/.config.env"
echo ""
echo "[OK] Configured as: $DISPLAY_NAME"
echo ""

# 3. Virtual environment setup
if [ ! -d "$APP_DIR/.venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$APP_DIR/.venv"
fi

echo "Installing dependencies..."
"$APP_DIR/.venv/bin/pip" install --quiet -r "$APP_DIR/requirements.txt"

# 4. Safely reload launchd service
# Register background service
echo "Registering background service..."
launchctl bootout "gui/$(id -u)/${PLIST_LABEL}" 2>/dev/null || true
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
        <string>-m</string>
        <string>uvicorn</string>
        <string>app:app</string>
        <string>--port</string>
        <string>8000</string>
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
launchctl bootstrap "gui/$(id -u)" "$PLIST_PATH" 2>/dev/null || launchctl load "$PLIST_PATH"

echo ""
echo " Setup complete! App is running in the background."
echo "1. Open Safari and go to: http://localhost:8000"
echo "2. Click: File -> Add to Dock"
echo "3. It will default to: '$DISPLAY_NAME'"
