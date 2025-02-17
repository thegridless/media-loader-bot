from typing import Optional
from config.settings import BOT_TOKEN

class MediaBot:
    """Singleton bot class"""
    _instance: Optional['MediaBot'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.token = BOT_TOKEN 