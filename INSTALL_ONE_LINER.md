# One-Command Installation

## For Users

### Step 1: Install the System

Copy and paste this **single command** into Terminal to install Word of the Day:

```bash
cd ~ && git clone https://github.com/devashish-thakur/strokes-word-of-the-day.git strokes-wotd && cd strokes-wotd && chmod +x install.sh && ./install.sh
```

The system will:
1. Clone the repository to `~/strokes-wotd`
2. Automatically install and start the background daemon
3. Show you a beautiful Word of the Day in your browser every time you open your laptop lid

### Step 2: Grant Required Permissions

After installation, macOS will require you to grant permissions for the system to work:

#### **Option A: Grant via System Prompt (Recommended)**

1. **Test the installation** by running:
   ```bash
   cd ~/strokes-wotd && ./launch_word_of_day.sh
   ```

2. **When prompted**, click **"Allow"** or **"OK"** on any macOS permission dialogs that appear

3. macOS may show prompts for:
   - **Full Disk Access** (to read log files)
   - **Automation** (to open browser)

#### **Option B: Grant Manually**

If no prompts appear, grant permissions manually:

1. Open **System Settings** (or **System Preferences** on older macOS)

2. Navigate to **Privacy & Security**

3. Grant the following permissions:

   **For Terminal.app (or your terminal app):**
   - **Full Disk Access**: 
     - Click **Full Disk Access** in the left sidebar
     - Click the **+** button and add **Terminal.app** (found in `/Applications/Utilities/`)
     - Toggle it **ON**
   
   - **Automation** (if needed):
     - Click **Automation** in the left sidebar
     - Find **Terminal** and enable access to control your browser

4. **Restart Terminal** after granting permissions:
   ```bash
   # Close Terminal completely, then reopen and test:
   cd ~/strokes-wotd && ./launch_word_of_day.sh
   ```

### Step 3: Verify It Works

Test by closing and opening your laptop lid - your browser will open with a beautiful Word of the Day page!

---

## What It Does

- Downloads the project from GitHub
- Runs the installation script automatically
- Sets up a LaunchAgent that runs on Mac wake
- Starts monitoring immediately

---

## Troubleshooting

### Quick Diagnostics

Run the permission checker to diagnose issues:

```bash
cd ~/strokes-wotd && ./check_permissions.sh
```

This will check:
- LaunchAgent status
- File permissions
- Python availability
- Recent logs
- Required macOS permissions

### Browser Not Opening?

If the browser doesn't open when you wake your Mac:

1. **Run the permission checker** (see above) - it will tell you exactly what's wrong

2. **Check permissions are granted** (see Step 2 above)

3. **Restart the daemon** if needed:
   ```bash
   launchctl unload ~/Library/LaunchAgents/com.wordoftheday.wake.plist
   launchctl load ~/Library/LaunchAgents/com.wordoftheday.wake.plist
   ```

### Still Not Working?

- Make sure you've **completely closed and reopened Terminal** after granting permissions
- Try running manually first: `cd ~/strokes-wotd && ./launch_word_of_day.sh`
- Check if your Mac actually goes to sleep (some apps like Amphetamine prevent sleep)
- View detailed logs: `tail -50 /tmp/wordoftheday.log`

---

## Uninstall

```bash
launchctl unload ~/Library/LaunchAgents/com.wordoftheday.wake.plist && rm ~/Library/LaunchAgents/com.wordoftheday.wake.plist && rm -rf ~/strokes-wotd
```
