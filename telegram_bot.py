import os
import logging
import asyncio

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# Reuse BhashaAI's existing AI and language functions.
from app import call_ollama, detect_language_style

# Load environment variables from .env
load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Reduce noisy HTTP logs from Telegram.
logging.getLogger("httpx").setLevel(logging.WARNING)

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle /start command."""
    if update.message is None:
        return

    await update.message.reply_text(
        "Hi! 👋 I'm BhashaAI Customer Support.\n\n"
        "You can ask me about:\n"
        "🛍️ Products and prices\n"
        "📦 Available stock\n"
        "⭐ Membership and discounts\n"
        "🚚 Shipping and returns\n\n"
        "You can message me in English, Telugu, Tenglish, "
        "Hindi, or Hinglish."
    )


async def help_command(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Handle /help command."""
    if update.message is None:
        return

    await update.message.reply_text(
        "I'm BhashaAI, your store support assistant! 😊\n\n"
        "Try asking:\n"
        "• What products are available?\n"
        "• Explain membership\n"
        "• What is the price of Sonic Pro?\n"
        "• Naku membership details cheppu\n"
        "• Shipping policy kya hai?"
    )


async def handle_message(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Generate an AI reply to a text message."""
    if update.message is None or not update.message.text:
        return

    user_text = update.message.text.strip()

    if not user_text:
        return

    # Show that the bot is processing the message.
    await update.message.chat.send_action("typing")

    try:
        style = detect_language_style(user_text)

        # Use the existing BhashaAI system prompt and local Ollama model.
        # Run the blocking network request in a worker thread.
        reply = await asyncio.to_thread(
            call_ollama,
            [{"role": "user", "content": user_text[:8000]}],
            style,
        )

        reply = str(reply).strip()

        if not reply:
            reply = "Sorry, I couldn't generate a reply. Please try again."

        # Telegram messages have a maximum length of 4096 characters.
        # Send longer responses in smaller chunks.
        max_length = 4000

        for start_index in range(0, len(reply), max_length):
            await update.message.reply_text(
                reply[start_index:start_index + max_length]
            )

    except Exception:
        logging.exception("Telegram message handling failed")

        await update.message.reply_text(
            "Sorry, mama! 😅 BhashaAI couldn't process your message.\n"
            "Please check that Ollama is running and try again."
        )


async def error_handler(
    update: object,
    context: ContextTypes.DEFAULT_TYPE,
):
    """Log unexpected Telegram errors."""
    logging.error(
        "Telegram bot error",
        exc_info=(
            type(context.error),
            context.error,
            context.error.__traceback__,
        ) if context.error else None,
    )


def main():
    """Start the Telegram bot."""
    if not TOKEN:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is missing. "
            "Add your BotFather token to the project's .env file."
        )

    application = Application.builder().token(TOKEN).build()

    application.add_handler(
        CommandHandler("start", start)
    )

    application.add_handler(
        CommandHandler("help", help_command)
    )

    application.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            handle_message,
        )
    )

    application.add_error_handler(error_handler)

    print("BhashaAI Telegram bot is starting...")

    application.run_polling(
        allowed_updates=Update.ALL_TYPES
    )


if __name__ == "__main__":
    main()