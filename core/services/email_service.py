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

        print(f"Código gerado: {codigo_6_digitos}")

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

            print(f"[E-mail enviado para {receiver}] Código de recuperação: {codigo_6_digitos}")

            return codigo_6_digitos
        
        except Exception as e:
            print(f"[Erro no envio de e-mail] {e}")
            return None
        
    @staticmethod
    def send_vehicle_share_request(receiver, vehicle_plate):
        email_bot = os.getenv("EMAIL_BOT")
        senha_bot = os.getenv("SENHA_BOT")

        try:
            msg = EmailMessage()
            msg["From"] = email_bot
            msg["To"] = receiver
            msg["Subject"] = "Solicitação de Compartilhamento de Veículo"
            msg.set_content(f"Você recebeu uma solicitação para compartilhar o veículo {vehicle_plate}, verifique suas notificações no app. Caso não possua nenhum cadastro ignore essa mensagem", charset="utf-8")

            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                smtp.login(email_bot, senha_bot)
                smtp.send_message(msg)

            print(f"E-mail enviado para {receiver} sobre o veículo {vehicle_plate}.")
        except Exception as e:
            print(f"Erro ao enviar e-mail: {e}")