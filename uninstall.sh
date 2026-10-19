#!/bin/bash
PLIST_LABEL="com.$USER.commandcentre"
PLIST_PATH="$HOME/Library/LaunchAgents/${PLIST_LABEL}.plist"

echo "Stopping Command Centre..."
launchctl unload "$PLIST_PATH" 2>/dev/null || true
rm -f "$PLIST_PATH"

echo "Command Centre service removed."
