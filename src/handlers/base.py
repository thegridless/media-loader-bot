from abc import ABC, abstractmethod
from datetime import datetime
import os
from telegram import Update
from telegram.ext import ContextTypes
from config.settings import MEDIA_DIR
from core.bot import MediaBot

class MediaHandler(ABC):
    """Abstract base class for media handlers"""
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context
        self.bot_instance = MediaBot()
        
    @abstractmethod
    async def handle(self) -> bool:
        pass
    
    async def save_file(self, file, filename: str) -> None:
        file_path = os.path.join(MEDIA_DIR, filename)
        await file.download_to_drive(file_path)
    
    def get_file_metadata(self) -> tuple:
        user = self.update.effective_user
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        username = user.username or user.first_name or "unknown"
        return timestamp, username 