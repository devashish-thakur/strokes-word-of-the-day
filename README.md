# Word of the Day - macOS Wake Trigger

A production-quality tool that automatically displays a beautiful "Word of the Day" in your browser whenever your Mac wakes from sleep. Designed for daily habit formation with minimal friction.

## Features

- **Automatic Wake Detection**: Launches when you open your laptop lid
- **Beautiful HTML Display**: Modern, responsive design with smooth animations
- **Daily Persistence**: Same word all day, refreshes at midnight
- **Fast Execution**: <2 seconds from wake to display
- **Rich Content**: Each word includes pronunciation, meanings, examples, synonyms, antonyms, memory hooks
- **Streak Tracking**: Motivational streak counter for daily engagement
- **No Duplicates**: Intelligent lock mechanism prevents multiple tabs
- **50+ Words**: Curated vocabulary database with rich metadata

## Architecture

```
macOS Wake Event
    ↓
LaunchAgent (com.wordoftheday.wake.plist)
    ↓
Wrapper Script (launch_word_of_day.sh)
    ↓
Lock File Check (/tmp/wordoftheday.lock)
    ↓
Python Generator (main_html.py)
    ↓
HTML File Created (wordoftheday.html)
    ↓
Default Browser Opens with Beautiful Display
```

## Requirements

- macOS 10.15+ (tested on macOS 15.4)
- Python 3.7+ (tested with Python 3.12.0)
- Default web browser (Safari, Chrome, Firefox, etc.)

## Project Structure

```
strokes/
├── main_html.py            # Entry point
├── generate_html.py        # HTML/CSS generation
├── word_selector.py        # Daily word selection
├── state_manager.py        # Persistent state
├── data_loader.py          # JSON data handling
├── words.json              # 50+ word database
├── state.json              # Auto-generated state
├── wordoftheday.html       # Generated HTML page
├── launch_word_of_day.sh   # Wrapper script
├── wake_daemon.py          # Wake detection daemon
├── setup/
│   └── com.wordoftheday.wake.plist  # LaunchAgent config
└── README.md
```

## Installation

### Step 1: Copy LaunchAgent Configuration

```bash
cp setup/com.wordoftheday.wake.plist ~/Library/LaunchAgents/
```

### Step 2: Load the LaunchAgent

```bash
launchctl load ~/Library/LaunchAgents/com.wordoftheday.wake.plist
```

### Step 3: Test the Installation

```bash
# Run manually to verify everything works
./launch_word_of_day.sh
```

You should see your browser open with a beautiful Word of the Day page!

## Usage

### Automatic Usage

Once installed, the system runs automatically:

1. **Open your laptop lid** (wake from sleep)
2. Within 2-5 seconds, your browser opens with a beautiful Word of the Day page
3. The same word persists throughout the day
4. Tomorrow, you'll see a new word

### Manual Usage

You can also run the tool manually anytime:

```bash
# Show today's word in browser
./launch_word_of_day.sh

# Or generate HTML only
python3 main_html.py
open wordoftheday.html
```

## How It Works

### Wake Detection

Since macOS doesn't provide a native "on wake" trigger for LaunchAgents, we use a hybrid approach:

1. **RunAtLoad**: Triggers when the LaunchAgent loads (login, wake)
2. **StartInterval**: Polls every 5 minutes as a fallback
3. **Lock File**: Prevents duplicate executions within 10 seconds

### Daily Word Logic

```python
# Simplified logic flow
if today's_date != stored_date:
    increment_word_index()
    increment_streak()
    save_new_date()
else:
    use_same_word()
```

### State Management

The `state.json` file tracks:

```json
{
  "last_date": "2026-04-14",
  "current_word_index": 5,
  "streak_count": 12,
  "last_execution_timestamp": 1713097200
}
```

## Word Data Format

Each word in `words.json` includes:

```json
{
  "word": "ephemeral",
  "pronunciation": "ih-FEM-er-uhl",
  "part_of_speech": "adjective",
  "meaning": "Lasting for a very short time",
  "examples": {
    "casual": "That meme was totally ephemeral...",
    "formal": "The ephemeral nature of success...",
    "dramatic": "Like morning dew, ephemeral..."
  },
  "synonyms": ["fleeting", "transient", "momentary"],
  "antonyms": ["permanent", "eternal", "enduring"],
  "memory_hook": "Think ephemeral = temporary",
  "common_mistake": "Don't confuse with ethereal",
  "root": "Greek ephemeros (lasting a day)"
}
```

## Testing

### Test 1: Manual Execution

```bash
python3 main.py
```

**Expected**: Word of the Day displays with formatting

### Test 2: Wrapper Script

```bash
./launch_word_of_day.sh
```

**Expected**: New Terminal window opens with Word of the Day

### Test 3: LaunchAgent Status

```bash
launchctl list | grep wordoftheday
```

**Expected**: Shows the agent is loaded and running

### Test 4: Multiple Rapid Executions

```bash
./launch_word_of_day.sh
sleep 2
./launch_word_of_day.sh
```

**Expected**: Second execution skipped due to lock file

### Test 5: Wake from Sleep

1. Close your laptop lid (sleep)
2. Wait 30 seconds
3. Open laptop lid (wake)

**Expected**: Within 5-10 seconds, Terminal opens with Word of the Day

## Debugging

### Issue: Terminal Doesn't Open on Wake

**Check LaunchAgent Status:**

```bash
launchctl list | grep wordoftheday
```

Should show: `com.wordoftheday.wake` with a PID

**View Logs:**

```bash
# Wrapper script log
tail -f /tmp/wordoftheday.log

# LaunchAgent stdout
tail -f /tmp/wordoftheday_stdout.log

# LaunchAgent stderr
tail -f /tmp/wordoftheday_stderr.log

# Python error log
tail -f /tmp/wordoftheday_error.log
```

**Test Wrapper Script:**

```bash
bash -x ./launch_word_of_day.sh
```

**Common Fixes:**

1. **Python Path Issue**: Update Python path in `launch_word_of_day.sh`:
   ```bash
   which python3
   # Update PYTHON_BIN variable with the output
   ```

2. **Permissions Issue**: 
   ```bash
   chmod +x launch_word_of_day.sh
   chmod +x main.py
   ```

3. **Automation Permissions**: System Settings > Privacy > Automation > Terminal

### Issue: Python Script Errors

**Check File Existence:**

```bash
ls -la words.json state.json
```

**Test Python Modules:**

```bash
python3 -c "from data_loader import DataLoader; print('OK')"
python3 -c "from state_manager import StateManager; print('OK')"
python3 -c "from word_selector import WordSelector; print('OK')"
python3 -c "from display import WordDisplay; print('OK')"
```

**Validate JSON:**

```bash
python3 -m json.tool words.json > /dev/null && echo "words.json is valid"
python3 -m json.tool state.json > /dev/null && echo "state.json is valid"
```

### Issue: Same Word Every Day

**Check State File:**

```bash
cat state.json
```

**Reset State Manually:**

```bash
rm state.json
python3 main.py
```

### Issue: Duplicate Terminal Windows

**Check Lock File:**

```bash
ls -la /tmp/wordoftheday.lock
cat /tmp/wordoftheday.lock
```

**Clear Lock:**

```bash
rm /tmp/wordoftheday.lock
```

## Customization

### Change Cooldown Period

Edit `launch_word_of_day.sh`:

```bash
COOLDOWN_SECONDS=10  # Change to desired seconds
```

### Change Check Interval

Edit `setup/com.wordoftheday.wake.plist`:

```xml
<key>StartInterval</key>
<integer>300</integer>  <!-- Change to desired seconds -->
```

Then reload:

```bash
launchctl unload ~/Library/LaunchAgents/com.wordoftheday.wake.plist
launchctl load ~/Library/LaunchAgents/com.wordoftheday.wake.plist
```

### Add More Words

Edit `words.json` and add entries following the existing format. The word index will wrap around automatically.

### Customize Display

Edit `display.py` to change:
- Colors (add ANSI color codes)
- Layout (modify print methods)
- Width (change `self.width`)
- Emojis (modify emoji characters)

## Uninstalling

### Option 1: Disable (Keep Files)

```bash
# Unload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.wordoftheday.wake.plist
```

### Option 2: Complete Removal

```bash
# Unload LaunchAgent
launchctl unload ~/Library/LaunchAgents/com.wordoftheday.wake.plist

# Remove LaunchAgent
rm ~/Library/LaunchAgents/com.wordoftheday.wake.plist

# Remove project directory
cd ~
rm -rf /Users/devashish.thakur/strokes

# Remove temporary files
rm /tmp/wordoftheday.lock
rm /tmp/wordoftheday.log
rm /tmp/wordoftheday_stdout.log
rm /tmp/wordoftheday_stderr.log
rm /tmp/wordoftheday_error.log
```

## Re-enabling After Disable

```bash
launchctl load ~/Library/LaunchAgents/com.wordoftheday.wake.plist
```

## Performance

- **Startup Time**: ~0.5-1.5 seconds
- **Memory Usage**: ~30-50 MB (Python interpreter)
- **Disk Space**: <1 MB total
- **CPU Impact**: Negligible (runs briefly, then exits)

## Troubleshooting Quick Reference

| Problem | Solution |
|---------|----------|
| No terminal opens | Check LaunchAgent status: `launchctl list \| grep wordoftheday` |
| Python errors | Check logs: `tail -f /tmp/wordoftheday_error.log` |
| Wrong word | Delete `state.json` to reset |
| Duplicate windows | Increase `COOLDOWN_SECONDS` in wrapper script |
| Permission denied | Run `chmod +x launch_word_of_day.sh main.py` |
| JSON errors | Validate with `python3 -m json.tool words.json` |

## Advanced Configuration

### Running Only on Wake (Not Periodic)

Edit `setup/com.wordoftheday.wake.plist` and remove the `StartInterval` section, then reload.

**Note**: This makes the system less reliable as macOS doesn't have a native wake trigger.

### Custom Lock File Location

Edit `launch_word_of_day.sh`:

```bash
LOCK_FILE="$HOME/.wordoftheday.lock"  # Custom location
```

### Silent Mode (No Terminal Window)

Modify `launch_word_of_day.sh` to run Python directly without Terminal:

```bash
cd "$SCRIPT_DIR"
"$PYTHON_BIN" main.py >> "$LOG_FILE" 2>&1
```

**Note**: This defeats the purpose of displaying the word visibly!

## Security & Privacy

- **No Network Access**: All data is local
- **No Data Collection**: No analytics or tracking
- **No Sensitive Files**: Only reads/writes JSON state
- **Open Source**: All code is visible and auditable

## Contributing

To add more words, follow this format in `words.json`:

1. All fields are required except `common_mistake` and `root`
2. Use consistent formatting
3. Keep pronunciation accessible (not IPA)
4. Include 3 example types: casual, formal, dramatic
5. Add 3-5 synonyms and 3-5 antonyms
6. Create memorable memory hooks

## License

MIT License - Feel free to use, modify, and distribute.

## Support

For issues or questions:

1. Check the Debugging section above
2. Review log files in `/tmp/wordoftheday*.log`
3. Test components individually (Python, wrapper, LaunchAgent)

## Changelog

### v1.0.0 (2026-04-14)

- Initial release
- 50 curated words with rich metadata
- macOS wake detection via LaunchAgent
- Lock file mechanism for duplicate prevention
- Streak tracking for motivation
- Comprehensive error handling and logging

---

**Enjoy expanding your vocabulary, one day at a time!** 🚀📚✨
