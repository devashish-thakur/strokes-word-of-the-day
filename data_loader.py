"""
Data Loader Module
Handles loading and validating words from words.json
"""

import json
import os
from typing import List, Dict, Any


class DataLoader:
    """Loads and validates word data from JSON file"""
    
    def __init__(self, words_file: str = "words.json"):
        self.words_file = words_file
        self._words = None
    
    def load_words(self) -> List[Dict[str, Any]]:
        """
        Load words from JSON file with validation
        
        Returns:
            List of word dictionaries
            
        Raises:
            FileNotFoundError: If words.json doesn't exist
            ValueError: If JSON is invalid or empty
        """
        if not os.path.exists(self.words_file):
            raise FileNotFoundError(
                f"Words file not found: {self.words_file}\n"
                "Please ensure words.json exists in the same directory."
            )
        
        try:
            with open(self.words_file, 'r', encoding='utf-8') as f:
                words = json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in {self.words_file}: {e}")
        
        if not isinstance(words, list) or len(words) == 0:
            raise ValueError(f"{self.words_file} must contain a non-empty list of words")
        
        self._validate_words(words)
        self._words = words
        return words
    
    def _validate_words(self, words: List[Dict[str, Any]]) -> None:
        """
        Validate word structure
        
        Args:
            words: List of word dictionaries
            
        Raises:
            ValueError: If any word has missing required fields
        """
        required_fields = ['word', 'pronunciation', 'part_of_speech', 'meaning', 'examples']
        
        for idx, word_entry in enumerate(words):
            if not isinstance(word_entry, dict):
                raise ValueError(f"Word at index {idx} is not a dictionary")
            
            missing = [field for field in required_fields if field not in word_entry]
            if missing:
                raise ValueError(
                    f"Word at index {idx} ('{word_entry.get('word', 'unknown')}') "
                    f"is missing required fields: {', '.join(missing)}"
                )
    
    def get_word_count(self) -> int:
        """Get total number of words available"""
        if self._words is None:
            self.load_words()
        return len(self._words)
    
    def get_word_by_index(self, index: int) -> Dict[str, Any]:
        """
        Get a specific word by index
        
        Args:
            index: Word index (will wrap around if out of bounds)
            
        Returns:
            Word dictionary
        """
        if self._words is None:
            self.load_words()
        
        return self._words[index % len(self._words)]
