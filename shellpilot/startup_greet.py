from datetime import datetime
import urllib.request
import json
from pathlib import Path
from typing import Optional
import random


class Greeting:
    OFFLINE_QUOTES = [
        "💡 Don't watch the clock; do what it does. Keep going. — Sam Levenson",
        "🚀 The only way to do great work is to love what you do. — Steve Jobs",
        "🔥 Push yourself, because no one else is going to do it for you.",
        "🌱 Success doesn’t come from what you do occasionally. It comes from what you do consistently.",
        "📘 Learning never exhausts the mind. — Leonardo da Vinci",
    ]
    def __init__(self):
        self.assistan_name = self._get
        
    def greet(self):
        if not self._is_enabled():
            return

        print()
        print(f"{self.greeting} I’m {self.assistant_name}, your terminal assistant.")
        print(self._get_quote())
        print()
    def _get_assistance_name(self) -> str:
        path = Path(__file__).parent.parent / "assistant_name.txt"
        if path.exists():
            return path.read_text().strip().capitalize() + "Buddy"
        return "ShellPilot"
    
    def _get_time_greeting(self) -> str:
        hour = datetime().now().hour
        if 5 <= hour < 12:
            return "🌞 Good morning!"
        elif 12 <= hour < 18:
            return "🌤️ Good afternoon!"
        elif 18 <= hour < 22:
            return "🌙 Good evening!"
        else:
            return "🌌 Burning the midnight oil?"
        
    @staticmethod
    def _is_online() -> bool:
        try:
            urllib.request.urlopen("https://www.google.com",timeout=2)
            return True
        except:
            return False
        
    def _get_online_quote(self) -> Optional[str]:
        try:
           with urllib.request.urlopen("") as response:
               data = json.loads(response.read().decode())
               return f"💬 {data[0]['q']} — {data[0]['a']}"
        except:
            return False
    def _get_quote(self) -> str:
        if self._is_online():
            quote = self._get_online_quote()
            if quote:
                return quote
        return random.choice(self.OFFLINE_QUOTES)
    
    @staticmethod
    def _is_enabled() -> str:
        return Path.home().joinpath(".shellpilot_enabled").exists()
    
    
    

if __name__ == "__main__":
    assistant = Greeting()
    assistant.greet()
        