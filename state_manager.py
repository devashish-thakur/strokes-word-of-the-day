"""
State Manager Module
Handles persistent state for word selection and streak tracking
"""

import json
import os
import time
from datetime import datetime
from typing import Dict, Any, Optional


class StateManager:
    """Manages persistent state across executions"""
    
    def __init__(self, state_file: str = "state.json"):
        self.state_file = state_file
        self._state = None
    
    def load_state(self) -> Dict[str, Any]:
        """
        Load state from file, create default if doesn't exist
        
        Returns:
            State dictionary with keys: last_date, current_word_index, 
            streak_count, last_execution_timestamp
        """
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, 'r', encoding='utf-8') as f:
                    self._state = json.load(f)
                    
                if not self._validate_state(self._state):
                    self._state = self._create_default_state()
            except (json.JSONDecodeError, IOError):
                self._state = self._create_default_state()
        else:
            self._state = self._create_default_state()
        
        return self._state
    
    def _validate_state(self, state: Any) -> bool:
        """Validate state structure"""
        if not isinstance(state, dict):
            return False
        
        required_keys = ['last_date', 'current_word_index', 'streak_count']
        return all(key in state for key in required_keys)
    
    def _create_default_state(self) -> Dict[str, Any]:
        """Create default state structure"""
        return {
            'last_date': datetime.now().strftime('%Y-%m-%d'),
            'current_word_index': 0,
            'streak_count': 1,
            'last_execution_timestamp': int(time.time())
        }
    
    def save_state(self, state: Optional[Dict[str, Any]] = None) -> None:
        """
        Save state to file
        
        Args:
            state: State dictionary to save (uses internal state if None)
        """
        if state is None:
            state = self._state
        
        try:
            with open(self.state_file, 'w', encoding='utf-8') as f:
                json.dump(state, f, indent=2)
        except IOError as e:
            print(f"Warning: Could not save state: {e}")
    
    def update_for_new_day(self, word_count: int) -> Dict[str, Any]:
        """
        Update state for a new day
        
        Args:
            word_count: Total number of words available
            
        Returns:
            Updated state dictionary
        """
        if self._state is None:
            self.load_state()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        if self._state['last_date'] != today:
            self._state['current_word_index'] = (self._state['current_word_index'] + 1) % word_count
            self._state['streak_count'] += 1
            self._state['last_date'] = today
        
        self._state['last_execution_timestamp'] = int(time.time())
        self.save_state()
        
        return self._state
    
    def get_current_word_index(self) -> int:
        """Get current word index"""
        if self._state is None:
            self.load_state()
        return self._state['current_word_index']
    
    def get_streak_count(self) -> int:
        """Get current streak count"""
        if self._state is None:
            self.load_state()
        return self._state['streak_count']
    
    def get_last_execution_timestamp(self) -> int:
        """Get last execution timestamp"""
        if self._state is None:
            self.load_state()
        return self._state.get('last_execution_timestamp', 0)
    
    def should_execute(self, cooldown_seconds: int = 10) -> bool:
        """
        Check if enough time has passed since last execution
        
        Args:
            cooldown_seconds: Minimum seconds between executions
            
        Returns:
            True if should execute, False if in cooldown period
        """
        if self._state is None:
            self.load_state()
        
        last_time = self._state.get('last_execution_timestamp', 0)
        current_time = int(time.time())
        
        return (current_time - last_time) >= cooldown_seconds
