import os
import requests
from telegram import Update
from telegram.ext import ContextTypes

# Configuración de las URLs y credenciales
LOGIN_URL = "https://prenotami.esteri.it/Home/Login"
CHECK_URL = "https://prenotami.esteri.it/Services/Booking/224"
REDIRECT_URL = "https://prenotami.esteri.it/Services"
USERNAME = os.getenv("PRENOTA_USR")
PASSWORD = os.getenv("PRENOTA_PSW")

async def check_prenota(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Verifica la disponibilidad de turnos en el sitio Prenotami."""
    try:
        # Crear una sesión para mantener cookies
        session = requests.Session()

        # Encabezados necesarios
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded",
        }

        # Payload con los datos de inicio de sesión
        login_payload = {
            "Email": USERNAME,
            "Password": PASSWORD,
        }

        # Realizar la solicitud de inicio de sesión
        login_response = session.post(LOGIN_URL, data=login_payload, headers=headers)

        # Verificar si el inicio de sesión fue exitoso
        if login_response.status_code != 200 or "Login" in login_response.url:
            await update.message.reply_text("Error: No se pudo iniciar sesión en Prenotami.")
            return

        # Acceder a la página de disponibilidad de turnos
        check_response = session.get(CHECK_URL, allow_redirects=False)

        # Verificar el estado de la página
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

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Error al conectar con Prenotami: {str(e)}")