import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.n8n_handler import forward_to_n8n, forward_from_n8n
from utils.joke_util import joke

# ID personal al que se permite el comando /start
MY_USER_ID = int(os.getenv("MY_USER_ID"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para el comando /start."""
    user_id = update.effective_user.id
    if user_id == MY_USER_ID:
        await update.message.reply_text(f"¡Hola {update.effective_user.first_name}! Soy tu bot de Telegram.")
    else:
        await update.message.reply_text("¡Raja de acá, amiguero!")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Manejador para el comando /help."""
    await update.message.reply_text("Comandos disponibles:\n/start - Iniciar\n/help - Ayuda\n/chiste - Dime un chiste")

async def say_hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde a un saludo."""
    await update.message.reply_text(f"¡Hola {update.effective_user.first_name}!")

async def tell_joke(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Responde con un chiste."""   
    joke = joke()
    await update.message.reply_text(joke)

if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    # Agregar manejadores
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("chiste", tell_joke))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex("(?i)^hola$"), say_hello))  # Responde a "hola"
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, forward_to_n8n))  # Mensajes a n8n
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex("^n8n:"), forward_from_n8n))  # Mensajes de n8n

    app.run_polling()
