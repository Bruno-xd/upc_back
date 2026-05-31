import os
import smtplib

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def enviar_alerta(
    destinatario: str,
    asunto: str,
    mensaje: str
):

    correo = MIMEMultipart()

    correo["From"] = EMAIL_SENDER
    correo["To"] = destinatario
    correo["Subject"] = asunto

    correo.attach(
        MIMEText(
            mensaje,
            "plain",
            "utf-8"
        )
    )

    try:

        servidor = smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        )

        servidor.starttls()

        servidor.login(
            EMAIL_SENDER,
            EMAIL_PASSWORD
        )

        servidor.sendmail(
            EMAIL_SENDER,
            destinatario,
            correo.as_string()
        )

        servidor.quit()

        print(
            f"Correo enviado a {destinatario}"
        )

        return True

    except Exception as e:

        print(
            f"Error enviando correo: {e}"
        )

        return False