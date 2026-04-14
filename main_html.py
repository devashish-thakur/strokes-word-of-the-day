#!/usr/bin/env python3
"""
Word of the Day - HTML Entry Point
Generates HTML page and opens in browser
"""

import sys
import os
from pathlib import Path

from data_loader import DataLoader
from state_manager import StateManager
from word_selector import WordSelector
from generate_html import HTMLGenerator


def main() -> int:
    """
    Main entry point for Word of the Day HTML version
    
    Returns:
        Exit code (0 for success, 1 for error)
    """
    script_dir = Path(__file__).parent.resolve()
    os.chdir(script_dir)
    
    html_output = script_dir / "wordoftheday.html"
    
    try:
        data_loader = DataLoader(words_file="words.json")
        state_manager = StateManager(state_file="state.json")
        
        if not state_manager.should_execute(cooldown_seconds=3):
            return 0
        
        word_selector = WordSelector(data_loader, state_manager)
        
        word, streak = word_selector.get_todays_word()
        
        html_generator = HTMLGenerator()
        html_content = html_generator.generate_html(word, streak)
        
        # Write HTML file
        with open(html_output, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"HTML generated: {html_output}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
