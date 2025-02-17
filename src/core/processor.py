from telegram import Update
from telegram.ext import ContextTypes
from handlers.media_handlers import PhotoHandler, VideoHandler, DocumentHandler

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