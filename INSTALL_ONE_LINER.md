# One-Command Installation

## For Users

Copy and paste this **single command** into Terminal to install Word of the Day:

```bash
cd ~ && git clone https://github.com/devashish-thakur/strokes-word-of-the-day.git strokes-wotd && cd strokes-wotd && chmod +x install.sh && ./install.sh
```

That's it! The system will:
1. Clone the repository to `~/strokes-wotd`
2. Automatically install and start the background daemon
3. Show you a beautiful Word of the Day in your browser every time you open your laptop lid

---

## What It Does

- Downloads the project from GitHub
- Runs the installation script automatically
- Sets up a LaunchAgent that runs on Mac wake
- Starts monitoring immediately

---

## Verification

After running the command, you should see:
```
✅ INSTALLATION COMPLETE
LaunchAgent: Running in background
```

Test it by closing and opening your laptop lid - your browser will open with a beautiful Word of the Day page!

---

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.wordoftheday.wake.plist && rm ~/Library/LaunchAgents/com.wordoftheday.wake.plist && rm -rf ~/strokes-wotd
```
