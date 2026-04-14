#!/usr/bin/env python3
"""
Word of the Day - Wake Detection Daemon
Uses macOS 'log stream' to monitor power events in real-time
Works on Apple Silicon with or without true sleep
"""

import sys
import os
import time
import subprocess
from datetime import datetime
from pathlib import Path


class WakeDetector:
    """Detects display wake events using log stream"""
    
    def __init__(self):
        """Initialize the wake detector"""
        self.script_dir = Path(__file__).parent.resolve()
        self.log_file = Path("/tmp/wordoftheday_wake_daemon.log")
        self.last_trigger_time = 0
        self.min_trigger_interval = 3  # 3 seconds minimum between triggers
        
        self.log("Wake daemon initialized (log stream monitoring)")
    
    def log(self, message):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"[{timestamp}] {message}\n"
        
        try:
            with open(self.log_file, 'a') as f:
                f.write(log_entry)
        except Exception as e:
            print(f"Error logging: {e}", file=sys.stderr)
    
    def should_trigger(self):
        """Check if enough time passed since last trigger"""
        current_time = time.time()
        if current_time - self.last_trigger_time < self.min_trigger_interval:
            return False
        return True
    
    def trigger_word_display(self):
        """Trigger the word of the day display"""
        if not self.should_trigger():
            self.log("⏱️  Skipping - too soon since last trigger")
            return
        
        self.last_trigger_time = time.time()
        self.log("🚀 Triggering Word of the Day display...")
        
        try:
            launch_script = self.script_dir / "launch_word_of_day.sh"
            
            if not launch_script.exists():
                self.log(f"❌ Error: Launch script not found at {launch_script}")
                return
            
            # Execute in background
            subprocess.Popen(
                ["/bin/bash", str(launch_script)],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                start_new_session=True
            )
            
            self.log("✅ Word display triggered successfully")
                
        except Exception as e:
            self.log(f"❌ Error running launch script: {e}")
    
    def monitor_power_events(self):
        """Monitor system power events using log stream"""
        self.log("Starting log stream monitoring for power events...")
        self.log('Watching for display wake and power assertions')
        
        try:
            # Use log stream to monitor power management events in real-time
            # --predicate filters for power-related messages
            process = subprocess.Popen(
                [
                    "log", "stream",
                    "--style", "syslog",
                    "--predicate", 
                    'eventMessage CONTAINS "Display is turned on" OR '
                    'eventMessage CONTAINS "Wake from" OR '
                    'eventMessage CONTAINS "com.apple.powermanagement.lidopen"'
                ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            
            self.log("✨ Monitoring active - waiting for wake events...")
            
            for line in process.stdout:
                line_lower = line.lower()
                
                # Detect display wake or lid open events
                if ("display is turned on" in line_lower or 
                    "lidopen" in line_lower or
                    ("wake from" in line_lower and "lid" in line_lower)):
                    
                    self.log(f"🎉 WAKE EVENT DETECTED!")
                    self.log(f"   Event: {line.strip()[:100]}")
                    self.trigger_word_display()
            
        except Exception as e:
            self.log(f"❌ Error monitoring log stream: {e}")
            self.log(f"   Error type: {type(e).__name__}")
            raise
    
    def start(self):
        """Start the wake detector"""
        self.log("✨ Daemon ready - monitoring system logs for wake events")
        
        try:
            self.monitor_power_events()
        except KeyboardInterrupt:
            self.log("🛑 Daemon stopped by user")
        except Exception as e:
            self.log(f"💥 Fatal error: {e}")
            # Restart after a delay
            self.log("🔄 Restarting in 5 seconds...")
            time.sleep(5)
            self.start()


def main():
    """Main entry point"""
    detector = WakeDetector()
    detector.start()


if __name__ == "__main__":
    main()
