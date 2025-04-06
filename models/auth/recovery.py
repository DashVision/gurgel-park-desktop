from email import charset
from email.utils import formataddr
from math import e
import os, secrets, smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class Recovery:
    @staticmethod
    def send_recovery_code(receiver) -> str:
        code = secrets.randbelow(10**6)
        formated_code = str(code).zfill(6)

        email_bot = os.getenv("EMAIL_BOT")
        senha_bot = os.getenv("SENHA_BOT")

        try:
            msg = EmailMessage()
            msg["From"] = email_bot
            msg["To"] = receiver
            msg["Subject"] = "Recuperação de senha"

            msg.set_content(
                f"Seu código de recuperação do sistema Gurgel Park: {formated_code}",
                charset="utf-8"
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_bot, senha_bot)
                server.send_message(msg)

                print(f"Código de recuperação enviado: {formated_code}")
                return formated_code

        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return None