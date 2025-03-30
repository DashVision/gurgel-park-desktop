import smtplib
import secrets
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class CodeSenders:
    @staticmethod
    def sendCodes(destinatario):
        code = secrets.randbelow(10**6)
        six_digits_code = str(code).zfill(6)

        email_bot = os.getenv("EMAIL_BOT")
        senha_bot = os.getenv("SENHA_BOT")

        try:
            msg = EmailMessage()
            msg["From"] = email_bot
            msg["To"] = destinatario
            msg["Subject"] = "Recuperação de senha"
            
            msg.set_content(
                f"Seu código de recuperação é {six_digits_code}",
                charset="utf-8"
            )

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(email_bot, senha_bot)
                server.send_message(msg)
                return six_digits_code

        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return None