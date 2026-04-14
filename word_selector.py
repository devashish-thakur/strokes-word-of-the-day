"""
Word Selector Module
Handles daily word selection logic
"""

from datetime import datetime
from typing import Dict, Any
from data_loader import DataLoader
from state_manager import StateManager


class WordSelector:
    """Selects the appropriate word for the day"""
    
    def __init__(self, data_loader: DataLoader, state_manager: StateManager):
        self.data_loader = data_loader
        self.state_manager = state_manager
    
    def get_todays_word(self) -> tuple[Dict[str, Any], int]:
        """
        Get today's word and streak count
        
        Returns:
            Tuple of (word_dictionary, streak_count)
        """
        words = self.data_loader.load_words()
        word_count = len(words)
        
        state = self.state_manager.load_state()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if state['last_date'] != today:
            state = self.state_manager.update_for_new_day(word_count)
        else:
            self.state_manager.save_state()
        
        word_index = state['current_word_index']
        word = self.data_loader.get_word_by_index(word_index)
        streak = state['streak_count']
        
        return word, streak
