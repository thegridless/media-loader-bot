import os
from datetime import datetime
from abc import ABC, abstractmethod
from typing import Optional
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

class MediaBot:
    """Singleton bot class"""
    _instance: Optional['MediaBot'] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.media_dir = "media"
        self.token = '8180387680:AAEmUzb54ImMWAlVQB6nXRZRImAx08soKmU'
        os.makedirs(self.media_dir, exist_ok=True)

class MediaHandler(ABC):
    """Abstract base class for media handlers (Command pattern)"""
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context
        self.bot_instance = MediaBot()
        
    @abstractmethod
    async def handle(self) -> bool:
        pass
    
    async def save_file(self, file, filename: str) -> None:
        file_path = os.path.join(self.bot_instance.media_dir, filename)
        await file.download_to_drive(file_path)
    
    def get_file_metadata(self) -> tuple:
        user = self.update.effective_user
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        username = user.username or user.first_name or "unknown"
        return timestamp, username

class PhotoHandler(MediaHandler):
    async def handle(self) -> bool:
        if not self.update.message.photo:
            return False
            
        timestamp, username = self.get_file_metadata()
        photo = self.update.message.photo[-1]
        file = await self.context.bot.get_file(photo.file_id)
        await self.save_file(file, f"{timestamp}_{username}_photo.jpg")
        return True

class VideoHandler(MediaHandler):
    async def handle(self) -> bool:
        if not self.update.message.video:
            return False
            
        timestamp, username = self.get_file_metadata()
        video = self.update.message.video
        file = await self.context.bot.get_file(video.file_id)
        extension = video.mime_type.split('/')[-1]
        await self.save_file(file, f"{timestamp}_{username}_video.{extension}")
        return True

class DocumentHandler(MediaHandler):
    async def handle(self) -> bool:
        if not self.update.message.document:
            return False
            
        timestamp, username = self.get_file_metadata()
        doc = self.update.message.document
        file = await self.context.bot.get_file(doc.file_id)
        await self.save_file(file, f"{timestamp}_{username}_{doc.file_name}")
        return True

class MediaProcessor:
    """Facade pattern for processing media"""
    def __init__(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        self.update = update
        self.context = context
        self.handlers = [
            PhotoHandler(update, context),
            VideoHandler(update, context),
            DocumentHandler(update, context)
        ]
    
    async def process(self) -> None:
        for handler in self.handlers:
            if await handler.handle():
                await self._send_success_message()
                return
        await self._send_error_message()
    
    async def _send_success_message(self) -> None:
        username = self.update.effective_user.username or self.update.effective_user.first_name or "unknown"
        await self.update.message.delete()
        await self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text=f"Media saved successfully from {username}!"
        )
    
    async def _send_error_message(self) -> None:
        await self.update.message.delete()
        await self.context.bot.send_message(
            chat_id=self.update.effective_chat.id,
            text="Please send a photo, video, or document!"
        )

async def handle_media(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    processor = MediaProcessor(update, context)
    await processor.process()

async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.delete()
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Only photos, videos, and documents are allowed!"
    )

def main():
    bot = MediaBot()
    app = Application.builder().token(bot.token).build()
    
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO | filters.Document.ALL, handle_media))
    app.add_handler(MessageHandler(filters.ALL, handle_other))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main() 