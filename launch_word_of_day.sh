#!/bin/bash

###############################################################################
# Word of the Day - Wake Launch Wrapper Script
# 
# This script:
# 1. Implements lock file mechanism to prevent duplicate executions
# 2. Opens Terminal.app programmatically
# 3. Executes the Python CLI tool
# 4. Logs execution for debugging
###############################################################################

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="/tmp/wordoftheday.lock"
LOG_FILE="/tmp/wordoftheday.log"
PYTHON_SCRIPT="${SCRIPT_DIR}/main.py"
COOLDOWN_SECONDS=3  # 3 second cooldown only to prevent rapid duplicates

# Get Python path - use system Python to avoid pyenv lock issues
PYTHON_BIN="/usr/bin/python3"
# Fallback to pyenv if system Python doesn't exist
if [ ! -f "$PYTHON_BIN" ]; then
    PYTHON_BIN="python3"
fi

# Logging function
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

# Simple cooldown check - only show once per hour
if [ -f "$LOCK_FILE" ]; then
    LOCK_TIME=$(cat "$LOCK_FILE" 2>/dev/null || echo "0")
    CURRENT_TIME=$(date +%s)
    TIME_DIFF=$((CURRENT_TIME - LOCK_TIME))
    
    if [ "$TIME_DIFF" -lt "$COOLDOWN_SECONDS" ]; then
        # Within cooldown period, skip silently (no log spam)
        exit 0
    fi
fi

# Acquire lock
date +%s > "$LOCK_FILE"
log "Lock acquired, launching Word of the Day..."

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    log "ERROR: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

# Open Terminal and run the Python script
# Using osascript to programmatically open Terminal and execute command
osascript <<EOF
tell application "Terminal"
    set newTab to do script "cd \"${SCRIPT_DIR}\" && ${PYTHON_BIN} main.py; echo ''; echo 'Press Enter to close...'; read; exit"
    activate
    repeat
        delay 0.5
        if not busy of newTab then
            close (window 1 whose tabs contains newTab)
            exit repeat
        end if
    end repeat
end tell
EOF

if [ $? -eq 0 ]; then
    log "Terminal opened successfully with Word of the Day"
    # Also log to file for reference
    cd "$SCRIPT_DIR"
    "$PYTHON_BIN" main.py >> /tmp/wordoftheday_output.log 2>&1
else
    log "ERROR: Failed to open Terminal"
    exit 1
fi

# Update lock file with current timestamp
date +%s > "$LOCK_FILE"
log "Execution complete"

exit 0
