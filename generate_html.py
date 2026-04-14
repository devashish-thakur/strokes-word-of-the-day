"""
HTML Generator Module
Generates beautiful HTML page for Word of the Day
"""

from typing import Dict, Any
from datetime import datetime


class HTMLGenerator:
    """Generates HTML page with word information"""
    
    def generate_html(self, word_data: Dict[str, Any], streak: int = 1) -> str:
        """
        Generate HTML page for the word
        
        Args:
            word_data: Dictionary containing word information
            streak: Current streak count
            
        Returns:
            Complete HTML string
        """
        today = datetime.now().strftime("%A, %B %d, %Y")
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Word of the Day - {word_data['word'].title()}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Helvetica Neue', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        
        .container {{
            background: white;
            border-radius: 24px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
            max-width: 800px;
            width: 100%;
            padding: 48px;
            animation: slideUp 0.5s ease-out;
        }}
        
        @keyframes slideUp {{
            from {{
                opacity: 0;
                transform: translateY(30px);
            }}
            to {{
                opacity: 1;
                transform: translateY(0);
            }}
        }}
        
        .header {{
            text-align: center;
            margin-bottom: 40px;
            padding-bottom: 30px;
            border-bottom: 2px solid #f0f0f0;
        }}
        
        .date {{
            color: #667eea;
            font-size: 14px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 8px;
        }}
        
        .title {{
            color: #333;
            font-size: 18px;
            font-weight: 500;
            color: #666;
        }}
        
        .word-section {{
            text-align: center;
            margin-bottom: 40px;
        }}
        
        .main-word {{
            font-size: 64px;
            font-weight: 800;
            color: #667eea;
            margin-bottom: 12px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }}
        
        .pronunciation {{
            font-size: 24px;
            color: #888;
            font-style: italic;
            margin-bottom: 8px;
        }}
        
        .part-of-speech {{
            font-size: 16px;
            color: #999;
            font-weight: 500;
        }}
        
        .section {{
            margin-bottom: 32px;
        }}
        
        .section-title {{
            font-size: 18px;
            font-weight: 700;
            color: #333;
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
        }}
        
        .section-emoji {{
            font-size: 24px;
        }}
        
        .meaning-text {{
            font-size: 18px;
            line-height: 1.8;
            color: #444;
        }}
        
        .example {{
            background: #f8f9fa;
            padding: 16px 20px;
            border-radius: 12px;
            margin-bottom: 12px;
            border-left: 4px solid #667eea;
        }}
        
        .example-label {{
            font-size: 12px;
            font-weight: 700;
            color: #667eea;
            text-transform: uppercase;
            margin-bottom: 6px;
            letter-spacing: 0.5px;
        }}
        
        .example-text {{
            font-size: 16px;
            color: #555;
            line-height: 1.6;
        }}
        
        .word-list {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            font-size: 15px;
            color: #666;
        }}
        
        .word-tag {{
            background: #e8eaf6;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 500;
            color: #667eea;
        }}
        
        .memory-hook {{
            background: linear-gradient(135deg, #ffeaa7 0%, #fdcb6e 100%);
            padding: 20px;
            border-radius: 12px;
            font-size: 16px;
            color: #333;
            line-height: 1.6;
            border-left: 4px solid #fdcb6e;
        }}
        
        .info-box {{
            background: #fff3cd;
            padding: 16px;
            border-radius: 12px;
            font-size: 15px;
            color: #856404;
            margin-bottom: 12px;
            border-left: 4px solid #ffc107;
        }}
        
        .info-label {{
            font-weight: 700;
            margin-right: 6px;
        }}
        
        .streak {{
            text-align: center;
            margin-top: 40px;
            padding: 24px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border-radius: 12px;
            color: white;
        }}
        
        .streak-number {{
            font-size: 48px;
            font-weight: 800;
            margin-bottom: 8px;
        }}
        
        .streak-text {{
            font-size: 18px;
            opacity: 0.95;
        }}
        
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 30px;
            border-top: 2px solid #f0f0f0;
            font-size: 16px;
            color: #888;
        }}
        
        .footer-emoji {{
            font-size: 24px;
            margin-right: 8px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <div class="date">📅 {today}</div>
            <div class="title">Word of the Day</div>
        </div>
        
        <div class="word-section">
            <div class="main-word">{word_data['word']}</div>
            <div class="pronunciation">/{word_data['pronunciation']}/</div>
            <div class="part-of-speech">{word_data['part_of_speech']}</div>
        </div>
        
        <div class="section">
            <div class="section-title">
                <span class="section-emoji">📖</span>
                <span>Meaning</span>
            </div>
            <div class="meaning-text">{word_data['meaning']}</div>
        </div>
"""

        # Add examples
        if 'examples' in word_data:
            html += """
        <div class="section">
            <div class="section-title">
                <span class="section-emoji">🗣</span>
                <span>Examples</span>
            </div>
"""
            examples = word_data['examples']
            if 'casual' in examples:
                html += f"""
            <div class="example">
                <div class="example-label">Casual</div>
                <div class="example-text">{examples['casual']}</div>
            </div>
"""
            if 'formal' in examples:
                html += f"""
            <div class="example">
                <div class="example-label">Formal</div>
                <div class="example-text">{examples['formal']}</div>
            </div>
"""
            if 'dramatic' in examples:
                html += f"""
            <div class="example">
                <div class="example-label">Dramatic</div>
                <div class="example-text">{examples['dramatic']}</div>
            </div>
"""
            html += "        </div>\n"
        
        # Add synonyms
        if word_data.get('synonyms'):
            synonyms_html = ''.join([f'<span class="word-tag">{s}</span>' for s in word_data['synonyms'][:6]])
            html += f"""
        <div class="section">
            <div class="section-title">
                <span class="section-emoji">🔁</span>
                <span>Synonyms</span>
            </div>
            <div class="word-list">
                {synonyms_html}
            </div>
        </div>
"""
        
        # Add antonyms
        if word_data.get('antonyms'):
            antonyms_html = ''.join([f'<span class="word-tag">{a}</span>' for a in word_data['antonyms'][:6]])
            html += f"""
        <div class="section">
            <div class="section-title">
                <span class="section-emoji">🔄</span>
                <span>Antonyms</span>
            </div>
            <div class="word-list">
                {antonyms_html}
            </div>
        </div>
"""
        
        # Add memory hook
        if word_data.get('memory_hook'):
            html += f"""
        <div class="section">
            <div class="section-title">
                <span class="section-emoji">💡</span>
                <span>Memory Hook</span>
            </div>
            <div class="memory-hook">{word_data['memory_hook']}</div>
        </div>
"""
        
        # Add common mistake
        if word_data.get('common_mistake'):
            html += f"""
            <div class="info-box">
                <span class="info-label">⚠️ Common Mistake:</span>
                {word_data['common_mistake']}
            </div>
"""
        
        # Add etymology
        if word_data.get('root'):
            html += f"""
            <div class="info-box">
                <span class="info-label">🌱 Etymology:</span>
                {word_data['root']}
            </div>
"""
        
        # Add streak
        if streak > 1:
            fire_emojis = "🔥" * min(streak, 10)
            html += f"""
        <div class="streak">
            <div class="streak-number">{streak} Days {fire_emojis}</div>
            <div class="streak-text">Daily Learning Streak</div>
        </div>
"""
        
        # Footer
        html += """
        <div class="footer">
            <span class="footer-emoji">💪</span>
            Keep learning, one word at a time!
        </div>
    </div>
</body>
</html>
"""
        
        return html
