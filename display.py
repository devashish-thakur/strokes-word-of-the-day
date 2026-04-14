"""
Display Module
Handles rich formatting and terminal output for the word of the day
"""

from typing import Dict, Any
from datetime import datetime


class WordDisplay:
    """Formats and displays word information"""
    
    def __init__(self):
        self.width = 70
    
    def _print_separator(self, char: str = "─") -> None:
        """Print a separator line"""
        print(char * self.width)
    
    def _print_header(self) -> None:
        """Print the header section"""
        print("\n")
        self._print_separator("═")
        today = datetime.now().strftime("%A, %B %d, %Y")
        print(f"📅  WORD OF THE DAY  •  {today}".center(self.width))
        self._print_separator("═")
        print()
    
    def _print_word_title(self, word: str, pronunciation: str, pos: str) -> None:
        """Print the main word with pronunciation and part of speech"""
        print(f"✨  {word.upper()}")
        print(f"    /{pronunciation}/")
        print(f"    ({pos})")
        print()
    
    def _print_meaning(self, meaning: str) -> None:
        """Print the word meaning"""
        print("📖  Meaning:")
        print(f"    {meaning}")
        print()
    
    def _print_examples(self, examples: Dict[str, str]) -> None:
        """Print usage examples"""
        print("🗣  Examples:")
        
        if 'casual' in examples:
            print(f"    • Casual:  {examples['casual']}")
        
        if 'formal' in examples:
            print(f"    • Formal:  {examples['formal']}")
        
        if 'dramatic' in examples:
            print(f"    • Dramatic: {examples['dramatic']}")
        
        print()
    
    def _print_synonyms_antonyms(self, synonyms: list, antonyms: list) -> None:
        """Print synonyms and antonyms"""
        if synonyms:
            synonyms_str = ", ".join(synonyms[:5])
            print(f"🔁  Synonyms: {synonyms_str}")
        
        if antonyms:
            antonyms_str = ", ".join(antonyms[:5])
            print(f"🔄  Antonyms: {antonyms_str}")
        
        if synonyms or antonyms:
            print()
    
    def _print_memory_hook(self, memory_hook: str) -> None:
        """Print memory hook"""
        if memory_hook:
            print("💡  Memory Hook:")
            print(f"    {memory_hook}")
            print()
    
    def _print_additional_info(self, word_data: Dict[str, Any]) -> None:
        """Print additional information like common mistakes and root"""
        has_info = False
        
        if word_data.get('common_mistake'):
            print(f"⚠️   Common Mistake: {word_data['common_mistake']}")
            has_info = True
        
        if word_data.get('root'):
            print(f"🌱  Etymology: {word_data['root']}")
            has_info = True
        
        if has_info:
            print()
    
    def _print_streak(self, streak: int) -> None:
        """Print streak information"""
        if streak > 1:
            fire_emojis = "🔥" * min(streak, 10)
            print(f"🎯  Daily Streak: {streak} days {fire_emojis}")
            print()
    
    def _print_footer(self) -> None:
        """Print footer"""
        self._print_separator("─")
        print("💪  Keep learning, one word at a time!".center(self.width))
        self._print_separator("═")
        print("\n")
    
    def display_word(self, word_data: Dict[str, Any], streak: int = 1) -> None:
        """
        Display the complete word information
        
        Args:
            word_data: Dictionary containing word information
            streak: Current streak count
        """
        self._print_header()
        
        self._print_word_title(
            word_data['word'],
            word_data['pronunciation'],
            word_data['part_of_speech']
        )
        
        self._print_meaning(word_data['meaning'])
        
        if 'examples' in word_data:
            self._print_examples(word_data['examples'])
        
        self._print_synonyms_antonyms(
            word_data.get('synonyms', []),
            word_data.get('antonyms', [])
        )
        
        if word_data.get('memory_hook'):
            self._print_memory_hook(word_data['memory_hook'])
        
        self._print_additional_info(word_data)
        
        self._print_streak(streak)
        
        self._print_footer()
    
    def display_error(self, error_message: str) -> None:
        """
        Display an error message
        
        Args:
            error_message: Error message to display
        """
        print("\n")
        self._print_separator("═")
        print("❌  ERROR".center(self.width))
        self._print_separator("═")
        print()
        print(f"    {error_message}")
        print()
        self._print_separator("═")
        print("\n")
