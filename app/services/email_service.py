import os
import smtplib

from dotenv import load_dotenv

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

load_dotenv()

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")


def enviar_alerta(
    destinatario: str,
    asunto: str,
    mensaje: str,
    archivo_adjunto: str = None
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

    # =====================================
    # ADJUNTAR PDF
    # =====================================
    if archivo_adjunto and os.path.exists(archivo_adjunto):

        with open(archivo_adjunto, "rb") as archivo:

            parte = MIMEBase(
                "application",
                "octet-stream"
            )

            parte.set_payload(
                archivo.read()
            )

        encoders.encode_base64(parte)

        parte.add_header(
            "Content-Disposition",
            f'attachment; filename="{os.path.basename(archivo_adjunto)}"'
        )

        correo.attach(parte)

    try:

        with smtplib.SMTP(
            SMTP_SERVER,
            SMTP_PORT
        ) as servidor:

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

        print(
            f"Correo enviado a {destinatario}"
        )

        return True

    except Exception as e:

        print(
            f"Error enviando correo: {e}"
        )

        return False