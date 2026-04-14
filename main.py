#!/usr/bin/env python3
"""
Word of the Day - Main Entry Point
Displays a daily vocabulary word with rich formatting
"""

import sys
import os
from pathlib import Path

from data_loader import DataLoader
from state_manager import StateManager
from word_selector import WordSelector
from display import WordDisplay


def log_error(message: str) -> None:
    """Log error to file for debugging"""
    error_log = "/tmp/wordoftheday_error.log"
    try:
        with open(error_log, 'a') as f:
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"[{timestamp}] {message}\n")
    except:
        pass


def main() -> int:
    """
    Main entry point for Word of the Day CLI
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    
    display = WordDisplay()
    
    try:
        data_loader = DataLoader(words_file="words.json")
        state_manager = StateManager(state_file="state.json")
        
        if not state_manager.should_execute(cooldown_seconds=10):
            return 0
        
        word_selector = WordSelector(data_loader, state_manager)
        
        word, streak = word_selector.get_todays_word()
        
        display.display_word(word, streak)
        
        return 0
        
    except FileNotFoundError as e:
        error_msg = f"Missing file: {e}"
        display.display_error(error_msg)
        log_error(error_msg)
        return 1
        
    except ValueError as e:
        error_msg = f"Invalid data: {e}"
        display.display_error(error_msg)
        log_error(error_msg)
        return 1
        
    except Exception as e:
        error_msg = f"Unexpected error: {type(e).__name__}: {e}"
        display.display_error(error_msg)
        log_error(error_msg)
        return 1


if __name__ == "__main__":
    sys.exit(main())
