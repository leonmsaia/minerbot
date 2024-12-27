from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f"¡Hola {update.effective_user.first_name}! Soy tu bot de Telegram.")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Comandos disponibles:\n/start - Iniciar\n/help - Ayuda")

if __name__ == "__main__":
    import os
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.run_polling()
