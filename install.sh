#!/bin/bash

###############################################################################
# Word of the Day - One-Command Installation
# 
# This script installs and starts the Word of the Day system as a background
# LaunchAgent that runs indefinitely, automatically showing a word when your
# Mac wakes from sleep.
###############################################################################

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_FILE="com.wordoftheday.wake.plist"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_PATH="$LAUNCH_AGENT_DIR/$PLIST_FILE"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     Word of the Day - One-Command Installation & Startup        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Step 1: Verify files exist
echo "→ Verifying installation files..."
if [ ! -f "$SCRIPT_DIR/setup/$PLIST_FILE" ]; then
    echo "✗ Error: setup/$PLIST_FILE not found"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/launch_word_of_day.sh" ]; then
    echo "✗ Error: launch_word_of_day.sh not found"
    exit 1
fi

if [ ! -f "$SCRIPT_DIR/main.py" ]; then
    echo "✗ Error: main.py not found"
    exit 1
fi

echo "✓ All required files present"

# Step 2: Ensure scripts are executable
echo "→ Setting executable permissions..."
chmod +x "$SCRIPT_DIR/launch_word_of_day.sh"
chmod +x "$SCRIPT_DIR/main.py"
echo "✓ Permissions set"

# Step 3: Unload existing LaunchAgent if present
if [ -f "$LAUNCH_AGENT_PATH" ]; then
    echo "→ Unloading existing LaunchAgent..."
    launchctl unload "$LAUNCH_AGENT_PATH" 2>/dev/null || true
    echo "✓ Existing LaunchAgent unloaded"
fi

# Step 4: Copy LaunchAgent plist
echo "→ Installing LaunchAgent..."
mkdir -p "$LAUNCH_AGENT_DIR"
cp "$SCRIPT_DIR/setup/$PLIST_FILE" "$LAUNCH_AGENT_PATH"
echo "✓ LaunchAgent installed to $LAUNCH_AGENT_PATH"

# Step 5: Load LaunchAgent
echo "→ Starting LaunchAgent (will run in background indefinitely)..."
launchctl load "$LAUNCH_AGENT_PATH"
echo "✓ LaunchAgent loaded and running"

# Step 6: Verify it's running
sleep 1
if launchctl list | grep -q "com.wordoftheday.wake"; then
    echo "✓ LaunchAgent verified running"
else
    echo "⚠ Warning: LaunchAgent may not be running. Check status with:"
    echo "  launchctl list | grep wordoftheday"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ INSTALLATION COMPLETE                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 System Status:"
echo "   • LaunchAgent:  Running in background"
echo "   • Trigger:      Mac wake from sleep + every 5 minutes"
echo "   • Persistence:  Will restart on reboot"
echo ""
echo "🧪 Test Now:"
echo "   ./launch_word_of_day.sh"
echo ""
echo "📊 Check Status:"
echo "   launchctl list | grep wordoftheday"
echo ""
echo "📝 View Logs:"
echo "   tail -f /tmp/wordoftheday.log"
echo ""
echo "🛑 To Uninstall:"
echo "   launchctl unload ~/Library/LaunchAgents/$PLIST_FILE"
echo "   rm ~/Library/LaunchAgents/$PLIST_FILE"
echo ""
echo "✨ The system is now running! Close your laptop lid, wait 30 seconds,"
echo "   then open it to see your Word of the Day! 🎉"
echo ""
