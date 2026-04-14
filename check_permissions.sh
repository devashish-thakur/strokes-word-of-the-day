#!/bin/bash

###############################################################################
# Permission Checker for Word of the Day
# 
# This script helps diagnose permission issues
###############################################################################

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║          Word of the Day - Permission Checker                   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Check if LaunchAgent is running
echo "→ Checking LaunchAgent status..."
if launchctl list | grep -q "com.wordoftheday.wake"; then
    echo "✓ LaunchAgent is running"
else
    echo "✗ LaunchAgent is NOT running"
    echo "  Fix: launchctl load ~/Library/LaunchAgents/com.wordoftheday.wake.plist"
fi
echo ""

# Check if required files exist
echo "→ Checking required files..."
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

files=("launch_word_of_day.sh" "main_html.py" "wake_daemon.py" "words.json" "data_loader.py" "state_manager.py" "word_selector.py" "generate_html.py")

all_files_exist=true
for file in "${files[@]}"; do
    if [ -f "$SCRIPT_DIR/$file" ]; then
        echo "  ✓ $file"
    else
        echo "  ✗ $file (MISSING)"
        all_files_exist=false
    fi
done

if $all_files_exist; then
    echo "✓ All required files present"
else
    echo "✗ Some files are missing - reinstall may be needed"
fi
echo ""

# Check if scripts are executable
echo "→ Checking executable permissions..."
if [ -x "$SCRIPT_DIR/launch_word_of_day.sh" ]; then
    echo "✓ launch_word_of_day.sh is executable"
else
    echo "✗ launch_word_of_day.sh is NOT executable"
    echo "  Fix: chmod +x $SCRIPT_DIR/launch_word_of_day.sh"
fi

if [ -x "$SCRIPT_DIR/main_html.py" ]; then
    echo "✓ main_html.py is executable"
else
    echo "✗ main_html.py is NOT executable"
    echo "  Fix: chmod +x $SCRIPT_DIR/main_html.py"
fi

if [ -x "$SCRIPT_DIR/wake_daemon.py" ]; then
    echo "✓ wake_daemon.py is executable"
else
    echo "✗ wake_daemon.py is NOT executable"
    echo "  Fix: chmod +x $SCRIPT_DIR/wake_daemon.py"
fi
echo ""

# Check Python availability
echo "→ Checking Python..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version 2>&1)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python3 not found"
fi
echo ""

# Check log files
echo "→ Checking recent logs..."
if [ -f "/tmp/wordoftheday.log" ]; then
    echo "✓ Main log exists: /tmp/wordoftheday.log"
    echo "  Last 3 entries:"
    tail -3 /tmp/wordoftheday.log | sed 's/^/  /'
else
    echo "⚠ No main log found (system hasn't run yet)"
fi
echo ""

if [ -f "/tmp/wake_daemon.log" ]; then
    echo "✓ Wake daemon log exists: /tmp/wake_daemon.log"
    echo "  Last 3 entries:"
    tail -3 /tmp/wake_daemon.log | sed 's/^/  /'
else
    echo "⚠ No wake daemon log found"
fi
echo ""

# Provide permission guidance
echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║                    macOS Permissions Required                   ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""
echo "To grant permissions:"
echo ""
echo "1. Open System Settings > Privacy & Security"
echo ""
echo "2. Click 'Full Disk Access' and add Terminal.app:"
echo "   • Click the '+' button"
echo "   • Navigate to /Applications/Utilities/Terminal.app"
echo "   • Toggle it ON"
echo ""
echo "3. Click 'Automation' (if needed) and enable:"
echo "   • Terminal → [Your Browser]"
echo ""
echo "4. Restart Terminal completely after granting permissions"
echo ""
echo "5. Test manually:"
echo "   cd $(pwd) && ./launch_word_of_day.sh"
echo ""
