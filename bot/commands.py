from telegram import Update
from telegram.ext import ContextTypes


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send welcome message with command list and general usage scenario."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text='Hello!'
    )
