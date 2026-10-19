#!/bin/bash
set -e

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_LABEL="com.$USER.commandcentre"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"

echo "========================================"
echo "      Uninstalling Command Centre       "
echo "========================================"
echo ""

# 1. Stop and remove macOS background service
echo "Stopping background service..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true
rm -f "$PLIST_PATH"

# 2. Terminate any lingering processes on port 8000
kill -9 $(lsof -t -i:8000) 2>/dev/null || true

echo "Background service removed."
echo ""

# 3. Prompt user about data retention
echo "How would you like to handle your data?"
echo "  [1] Keep my database (Tasks, notes, and tags will reload if you reinstall) [Default]"
echo "  [2] Nuclear Wipe (Permanently delete database, config, virtual environment, and logs)"
read -p "Select an option (1 or 2, default is 1): " UNINSTALL_CHOICE

if [ "$UNINSTALL_CHOICE" = "2" ]; then
    echo ""
    read -p "Are you sure? This CANNOT be undone! Type 'DELETE' to confirm: " CONFIRM_DELETE
    if [ "$CONFIRM_DELETE" = "DELETE" ]; then
        echo "Performing complete purge..."
        rm -rf "$APP_DIR/.venv"
        rm -rf "$APP_DIR/__pycache__"
        rm -f "$APP_DIR"/*.db "$APP_DIR"/*.sqlite3
        rm -f "$APP_DIR/.config.env"
        rm -f "$APP_DIR"/*.log
        echo "All user data, virtual environments, and local files have been purged."
    else
        echo "Confirmation mismatch. Data preserved safely."
    fi
else
    echo "Database and notes kept safe."
fi

echo ""
echo "========================================"
echo "Uninstallation complete."
echo "========================================"
