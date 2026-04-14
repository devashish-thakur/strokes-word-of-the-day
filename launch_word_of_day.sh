#!/bin/bash

###############################################################################
# Word of the Day - Wake Launch Wrapper Script
# 
# This script:
# 1. Implements lock file mechanism to prevent duplicate executions
# 2. Generates HTML page with word
# 3. Opens in default browser
# 4. Logs execution for debugging
###############################################################################

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOCK_FILE="/tmp/wordoftheday.lock"
LOG_FILE="/tmp/wordoftheday.log"
PYTHON_SCRIPT="${SCRIPT_DIR}/main_html.py"
HTML_OUTPUT="${SCRIPT_DIR}/wordoftheday.html"
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

# Simple cooldown check
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
log "Lock acquired, generating Word of the Day HTML..."

# Check if Python script exists
if [ ! -f "$PYTHON_SCRIPT" ]; then
    log "ERROR: Python script not found at $PYTHON_SCRIPT"
    exit 1
fi

# Generate HTML
cd "$SCRIPT_DIR"
"$PYTHON_BIN" main_html.py >> /tmp/wordoftheday_output.log 2>&1

if [ $? -eq 0 ]; then
    log "HTML generated successfully"
else
    log "ERROR: Failed to generate HTML"
    exit 1
fi

# Open in default browser
if [ -f "$HTML_OUTPUT" ]; then
    open "$HTML_OUTPUT"
    log "Browser opened with Word of the Day"
else
    log "ERROR: HTML file not found at $HTML_OUTPUT"
    exit 1
fi

# Update lock file with current timestamp
date +%s > "$LOCK_FILE"
log "Execution complete"

exit 0
