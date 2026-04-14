#!/bin/bash

###############################################################################
# Word of the Day - One-Command Installation
#
# This script installs and starts the Word of the Day system as a background
# LaunchAgent that runs indefinitely, automatically showing a word in your
# browser when your Mac wakes from sleep.
#
# Works on any Mac - no hardcoded paths.
###############################################################################

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLIST_LABEL="com.wordoftheday.wake"
PLIST_FILE="${PLIST_LABEL}.plist"
LAUNCH_AGENT_DIR="$HOME/Library/LaunchAgents"
LAUNCH_AGENT_PATH="$LAUNCH_AGENT_DIR/$PLIST_FILE"

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║     Word of the Day - One-Command Installation & Startup        ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# ─── Step 1: Clean up any existing installation ──────────────────────────────
echo "→ Cleaning up any existing installation..."
launchctl unload "$LAUNCH_AGENT_PATH" 2>/dev/null || true
rm -f "$LAUNCH_AGENT_PATH"
rm -f /tmp/wordoftheday.lock
echo "✓ Clean slate ready"

# ─── Step 2: Detect Python 3 ─────────────────────────────────────────────────
echo "→ Detecting Python 3..."

PYTHON_BIN=""

# Priority order: system python3, homebrew, pyenv, fallback
for candidate in /usr/bin/python3 /usr/local/bin/python3 /opt/homebrew/bin/python3; do
    if [ -f "$candidate" ]; then
        PYTHON_BIN="$candidate"
        break
    fi
done

# Last resort: whatever is on PATH
if [ -z "$PYTHON_BIN" ]; then
    if command -v python3 &>/dev/null; then
        PYTHON_BIN="$(command -v python3)"
    fi
fi

if [ -z "$PYTHON_BIN" ]; then
    echo "✗ Error: Python 3 not found."
    echo "  Install it from https://www.python.org or via Homebrew: brew install python"
    exit 1
fi

PYTHON_VERSION=$("$PYTHON_BIN" --version 2>&1)
echo "✓ Python found: $PYTHON_VERSION at $PYTHON_BIN"

# ─── Step 3: Verify required files ───────────────────────────────────────────
echo "→ Verifying installation files..."

REQUIRED_FILES=(
    "launch_word_of_day.sh"
    "main_html.py"
    "generate_html.py"
    "wake_daemon.py"
    "data_loader.py"
    "state_manager.py"
    "word_selector.py"
    "words.json"
)

ALL_PRESENT=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$SCRIPT_DIR/$file" ]; then
        echo "✗ Error: $file not found"
        ALL_PRESENT=false
    fi
done

if [ "$ALL_PRESENT" = false ]; then
    echo "✗ Some required files are missing. Re-clone the repository."
    exit 1
fi

echo "✓ All required files present"

# ─── Step 4: Set executable permissions ──────────────────────────────────────
echo "→ Setting executable permissions..."
chmod +x "$SCRIPT_DIR/launch_word_of_day.sh"
chmod +x "$SCRIPT_DIR/main_html.py"
chmod +x "$SCRIPT_DIR/wake_daemon.py"
chmod +x "$SCRIPT_DIR/check_permissions.sh"
chmod +x "$SCRIPT_DIR/install.sh"
echo "✓ Permissions set"

# ─── Step 5: Test Python works ───────────────────────────────────────────────
echo "→ Testing Python and word generator..."
cd "$SCRIPT_DIR"
if "$PYTHON_BIN" main_html.py > /tmp/wordoftheday_install_test.log 2>&1; then
    echo "✓ Word generator works - HTML created successfully"
else
    echo "✗ Python test failed. Error:"
    cat /tmp/wordoftheday_install_test.log
    exit 1
fi

# ─── Step 6: Generate plist with correct paths for THIS machine ──────────────
echo "→ Generating LaunchAgent configuration..."
mkdir -p "$LAUNCH_AGENT_DIR"

cat > "$LAUNCH_AGENT_PATH" << PLIST_EOF
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>${PLIST_LABEL}</string>

    <key>ProgramArguments</key>
    <array>
        <string>${PYTHON_BIN}</string>
        <string>${SCRIPT_DIR}/wake_daemon.py</string>
    </array>

    <key>RunAtLoad</key>
    <true/>

    <key>KeepAlive</key>
    <true/>

    <key>StandardOutPath</key>
    <string>/tmp/wordoftheday_stdout.log</string>

    <key>StandardErrorPath</key>
    <string>/tmp/wordoftheday_stderr.log</string>

    <key>ProcessType</key>
    <string>Background</string>

    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/bin:/bin:/usr/local/bin:/opt/homebrew/bin:/usr/sbin:/sbin</string>
        <key>HOME</key>
        <string>${HOME}</string>
    </dict>
</dict>
</plist>
PLIST_EOF

echo "✓ LaunchAgent plist generated at $LAUNCH_AGENT_PATH"

# ─── Step 7: Load the LaunchAgent ────────────────────────────────────────────
echo "→ Loading LaunchAgent..."
launchctl load "$LAUNCH_AGENT_PATH"
echo "✓ LaunchAgent loaded"

# ─── Step 8: Verify it's running ─────────────────────────────────────────────
sleep 2
if launchctl list | grep -q "$PLIST_LABEL"; then
    echo "✓ LaunchAgent verified running"
else
    echo "⚠ Warning: LaunchAgent may not be running yet."
    echo "  Check: launchctl list | grep wordoftheday"
fi

# ─── Done ────────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    ✅ INSTALLATION COMPLETE                      ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "📋 Install Location:  $SCRIPT_DIR"
echo "🐍 Python Used:       $PYTHON_BIN"
echo ""
echo "🧪 Test it now:"
echo "   $SCRIPT_DIR/launch_word_of_day.sh"
echo ""
echo "📊 Run diagnostics:"
echo "   $SCRIPT_DIR/check_permissions.sh"
echo ""
echo "📝 View logs:"
echo "   tail -f /tmp/wordoftheday.log"
echo "   tail -f /tmp/wordoftheday_wake_daemon.log"
echo ""
echo "🛑 To uninstall:"
echo "   launchctl unload $LAUNCH_AGENT_PATH"
echo "   rm $LAUNCH_AGENT_PATH"
echo ""
echo "⚠️  GRANT PERMISSIONS (required for wake detection):"
echo "   System Settings → Privacy & Security → Full Disk Access"
echo "   → Click + and add Terminal.app → Toggle ON"
echo ""
echo "✨ Close your laptop lid, wait 30 seconds, open it -"
echo "   your browser will show the Word of the Day! 🎉"
echo ""
