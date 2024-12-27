import os
import requests
from telegram import Update
from telegram.ext import ContextTypes

# Configuración de las URLs y credenciales
LOGIN_URL = "https://prenotami.esteri.it/"
CHECK_URL = "https://prenotami.esteri.it/Services/Booking/224"
REDIRECT_URL = "https://prenotami.esteri.it/Services"
USERNAME = os.getenv("PRENOTA_USR")
PASSWORD = os.getenv("PRENOTA_PSW")

async def check_prenota(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Verifica la disponibilidad de turnos en el sitio Prenotami."""
    try:
        # Crear una sesión para mantener las cookies
        session = requests.Session()

        # Realizar el login
        login_payload = {
            "Email": USERNAME,
            "Password": PASSWORD,
        }
        login_response = session.post(LOGIN_URL, data=login_payload)

        if login_response.status_code != 200 or "Login" in login_response.url:
            await update.message.reply_text("Error: No se pudo iniciar sesión en Prenotami.")
            return

        # Acceder a la página de disponibilidad de turnos
        check_response = session.get(CHECK_URL, allow_redirects=False)

        if check_response.status_code == 302 and check_response.headers.get("Location") == REDIRECT_URL:
            await update.message.reply_text("No hay turnos disponibles en este momento.")
        elif check_response.status_code == 200:
            await update.message.reply_text(
                f"¡Turnos disponibles! Ingresa rápidamente: {CHECK_URL}"
            )
        else:
            await update.message.reply_text(
                f"Error desconocido al verificar turnos. Código de estado: {check_response.status_code}"
            )

    except Exception as e:
        await update.message.reply_text(f"Error al conectar con Prenotami: {str(e)}")
