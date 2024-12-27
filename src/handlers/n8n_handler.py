import os
import requests
from telegram import Update
from telegram.ext import ContextTypes

# URL del webhook de n8n
N8N_WEBHOOK_URL = os.getenv("N8N_WEBHOOK_URL")

# ID personal al que el bot reenviará mensajes desde n8n
MY_USER_ID = int(os.getenv("MY_USER_ID", "0"))

async def forward_to_n8n(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Envía el mensaje recibido al webhook de n8n."""
    user_message = update.message.text
    user_id = update.effective_user.id
    user_name = update.effective_user.first_name

    # Enviar el mensaje al webhook de n8n
    payload = {
        "user_id": user_id,
        "user_name": user_name,
        "message": user_message
    }

    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        if response.status_code == 200:
            await update.message.reply_text("Mensaje enviado a n8n correctamente.")
        else:
            await update.message.reply_text(f"Hubo un problema al enviar el mensaje a n8n: {response.status_code}")
    except Exception as e:
        await update.message.reply_text(f"Error al conectar con n8n: {str(e)}")

async def forward_from_n8n(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reenvía mensajes enviados desde n8n al usuario personal."""
    # Extraer mensaje enviado por n8n
    message = update.message.text

    if MY_USER_ID == 0:
        await update.message.reply_text("ID del usuario personal no configurado.")
        return

    try:
        await context.bot.send_message(chat_id=MY_USER_ID, text=f"Mensaje desde n8n:\n{message}")
        await update.message.reply_text("Mensaje reenviado correctamente.")
    except Exception as e:
        await update.message.reply_text(f"Error al reenviar el mensaje: {str(e)}")
