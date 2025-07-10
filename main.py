# Don't Remove Credit Tg - @Tushar0125
# Ask Doubt on telegram @Tushar0125

import os
import sys
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import FloodWait
from pdf2image import convert_from_path

from vars import API_ID, API_HASH, BOT_TOKEN

# Create uploads directory
if not os.path.exists("uploads"):
    os.makedirs("uploads")

# Bot client
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

OWNER_ID = 5840594311
SUDO_USERS = [OWNER_ID]


# Helper to check authorization
def is_authorized(user_id: int) -> bool:
    return user_id == OWNER_ID or user_id in SUDO_USERS


# Start command
@bot.on_message(filters.command("start"))
async def start_command(client: Client, message: Message):
    keyboard = InlineKeyboardMarkup(
        [[InlineKeyboardButton("💬 Contact Dev", url="https://t.me/Tushar0125")]]
    )
    await message.reply_text(
        "**👋 Welcome to TXT & PDF Uploader Bot!**\n\n"
        "📥 Send me a TXT or PDF file to upload.\n"
        "📸 For PDFs, thumbnails will be auto-generated!",
        reply_markup=keyboard
    )


# Upload TXT/PDF handler
@bot.on_message(filters.document)
async def handle_document(client: Client, message: Message):
    user_id = message.from_user.id
    if not is_authorized(user_id):
        await message.reply_text("🚫 You are not authorized to use this bot.")
        return

    file = message.document
    filename = file.file_name
    save_path = os.path.join("uploads", filename)

    await message.download(file_name=save_path)
    await message.reply_text(f"✅ File saved as `{filename}` in uploads folder.")

    # If it's a PDF, generate a thumbnail
    if filename.lower().endswith(".pdf"):
        try:
            images = convert_from_path(save_path, first_page=1, last_page=1)
            thumb_path = save_path.replace(".pdf", "_thumb.jpg")
            images[0].save(thumb_path, "JPEG")
            await client.send_photo(
                chat_id=message.chat.id,
                photo=thumb_path,
                caption=f"📸 Thumbnail for **{filename}**"
            )
        except Exception as e:
            await message.reply_text(f"⚠️ Failed to generate thumbnail: {e}")


# Stop bot
@bot.on_message(filters.command("stop"))
async def stop_command(client: Client, message: Message):
    await message.reply_text("🔴 Bot stopped.")
    sys.exit()


# Help command
@bot.on_message(filters.command("help"))
async def help_command(client: Client, message: Message):
    await message.reply_text(
        "**🆘 Help Menu**\n\n"
        "`/start` - Start the bot\n"
        "`/stop` - Stop the bot\n"
        "📥 Just send a TXT or PDF file to upload and get PDF thumbnail preview."
    )


# Run bot
bot.run()
