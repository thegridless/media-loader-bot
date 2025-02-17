import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Bot settings
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

# Media settings
MEDIA_DIR = os.getenv('MEDIA_DIR', 'media')
os.makedirs(MEDIA_DIR, exist_ok=True) 