import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from handlers.n8n_handler import forward_to_n8n, forward_from_n8n

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
    joke_api_url = "https://v2.jokeapi.dev/joke/Any"
    try:
        response = requests.get(joke_api_url)
        if response.status_code == 200:
            joke_data = response.json()
            if joke_data["type"] == "single":
                # Chiste de una sola línea
                joke = joke_data["joke"]
            elif joke_data["type"] == "twopart":
                # Chiste de dos partes
                joke = f'{joke_data["setup"]}\n{joke_data["delivery"]}'
            else:
                joke = "No pude encontrar un buen chiste esta vez."
        else:
            joke = f"Error al obtener el chiste: {response.status_code}"
    except Exception as e:
        joke = f"Error al conectar con JokeAPI: {str(e)}"
        
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
