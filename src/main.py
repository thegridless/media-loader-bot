from telegram.ext import Application, MessageHandler, filters
from core.bot import MediaBot
from core.processor import MediaProcessor

async def handle_media(update, context):
    processor = MediaProcessor(update, context)
    await processor.process()

async def handle_other(update, context):
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