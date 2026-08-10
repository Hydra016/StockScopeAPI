from typing import List
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig, MessageType
from utils.settings import settings

class MailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME = settings.MAIL_USERNAME,
            MAIL_PASSWORD = settings.MAIL_PASSWORD,
            MAIL_FROM = settings.MAIL_USERNAME,
            MAIL_PORT = 587,
            MAIL_SERVER = "smtp.gmail.com",
            MAIL_FROM_NAME="StockScope",
            MAIL_STARTTLS = True,
            MAIL_SSL_TLS = False,
            USE_CREDENTIALS = True,
            VALIDATE_CERTS = False
        )
        
    expiry_time = 60 * 10  # 10 mins in seconds

    async def send_verification_email(self, emails: List[str], code: str) -> dict[str, str]:
        html = f"""
        <div style="font-family: Arial, sans-serif; max-width: 480px; margin: 0 auto; padding: 24px;">
            <h2 style="color: #1a1a1a;">Verify your email</h2>
            <p style="color: #444; font-size: 15px;">
                Use the code below to verify your email address for StockScope.
            </p>
            <div style="background: #f4f4f4; border-radius: 8px; padding: 16px; text-align: center; margin: 24px 0;">
                <span style="font-size: 28px; font-weight: bold; letter-spacing: 4px; color: #1a1a1a;">
                    {code}
                </span>
            </div>
            <p style="color: #888; font-size: 13px;">
                This code will expire in 10 minutes. If you didn't request this, you can safely ignore this email.
            </p>
        </div>
        """

        message = MessageSchema(
            subject="Your StockScope verification code",
            recipients=emails,
            body=html,
            subtype=MessageType.html,
        )

        fm = FastMail(self.conf)
        await fm.send_message(message)
        return {"message": "Verification email sent"}
    
    async def send_confirmation_email(self, emails: List[str]):
        html = f"""<p>Welcome to StockScope! can't wait to see your trading progress!</p> """

        message = MessageSchema(
            subject="Welcome to StockScope",
            recipients=emails,
            body=html,
            subtype=MessageType.html)

        fm = FastMail(self.conf)
        await fm.send_message(message)
        return {"message": "email has been sent"}