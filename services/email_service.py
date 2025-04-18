import smtplib
import secrets
import os
from email.message import EmailMessage
from dotenv import load_dotenv

load_dotenv()

class EmailService:
    @staticmethod
    def send_recovery_code(receiver):
        code = secrets.randbelow(10**6)
        codigo_6_digitos = str(code).zfill(6)

        email_bot = os.getenv("EMAIL_BOT")
        senha_bot = os.getenv("SENHA_BOT")

        try:
            msg = EmailMessage()
            msg["From"] = email_bot
            msg["To"] = receiver
            msg["Subject"] = "Recuperação de senha"
            msg.set_content(f"Seu código de recuperação é: {codigo_6_digitos}", charset="utf-8")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_bot, senha_bot)
                smtp.send_message(msg)

            return codigo_6_digitos
        
        except Exception as e:
            print(f"[Erro no envio de e-mail] {e}")
            return None
        
        finally:
            msg.clear()
            smtp.quit()
            smtp.close()