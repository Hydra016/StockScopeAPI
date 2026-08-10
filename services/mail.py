from typing import Dict, List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType

from utils.settings import settings


class MailService:
    def __init__(self):
        self.conf = ConnectionConfig(
            MAIL_USERNAME=settings.MAIL_USERNAME,
            MAIL_PASSWORD=settings.MAIL_PASSWORD,
            MAIL_FROM=settings.MAIL_USERNAME,
            MAIL_PORT=587,
            MAIL_SERVER="smtp.gmail.com",
            MAIL_FROM_NAME="StockScope",
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=False,
        )
        self._fm = FastMail(self.conf)

    expiry_time = 60 * 10  # 10 mins in seconds

    def _wrap_email(self, title: str, body_html: str) -> str:
        return f"""
        <div style="margin:0;padding:0;background:#f0f2f5;">
          <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="background:#f0f2f5;padding:32px 16px;">
            <tr>
              <td align="center">
                <table role="presentation" width="100%" cellspacing="0" cellpadding="0" style="max-width:520px;background:#ffffff;border-radius:12px;overflow:hidden;border:1px solid #e5e7eb;">
                  <tr>
                    <td style="background:#0f172a;padding:20px 28px;">
                      <p style="margin:0;font-family:Arial,Helvetica,sans-serif;font-size:18px;font-weight:700;letter-spacing:0.3px;color:#ffffff;">
                        StockScope
                      </p>
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:28px;font-family:Arial,Helvetica,sans-serif;color:#1f2937;">
                      <h1 style="margin:0 0 12px;font-size:22px;line-height:1.3;color:#0f172a;">
                        {title}
                      </h1>
                      {body_html}
                    </td>
                  </tr>
                  <tr>
                    <td style="padding:16px 28px 24px;border-top:1px solid #eef2f7;font-family:Arial,Helvetica,sans-serif;font-size:12px;line-height:1.5;color:#9ca3af;">
                      You’re receiving this email because of activity on your StockScope account.
                      If this wasn’t you, you can ignore this message.
                    </td>
                  </tr>
                </table>
              </td>
            </tr>
          </table>
        </div>
        """

    async def send_verification_email(self, emails: List[str], code: str) -> Dict[str, str]:
        body = f"""
        <p style="margin:0 0 20px;font-size:15px;line-height:1.6;color:#4b5563;">
          Use the code below to verify your email and finish creating your StockScope account.
        </p>
        <div style="background:#f8fafc;border:1px solid #e2e8f0;border-radius:10px;padding:20px;text-align:center;margin:0 0 20px;">
          <p style="margin:0 0 8px;font-size:12px;letter-spacing:1px;text-transform:uppercase;color:#64748b;">
            Verification code
          </p>
          <p style="margin:0;font-size:32px;font-weight:700;letter-spacing:6px;color:#0f172a;">
            {code}
          </p>
        </div>
        <p style="margin:0;font-size:13px;line-height:1.6;color:#6b7280;">
          This code expires in <strong>10 minutes</strong>. Don’t share it with anyone.
        </p>
        """
        html = self._wrap_email("Verify your email", body)

        message = MessageSchema(
            subject="Your StockScope verification code",
            recipients=emails,
            body=html,
            subtype=MessageType.html,
        )
        await self._fm.send_message(message)
        return {"message": "Verification email sent"}

    async def send_confirmation_email(self, emails: List[str]) -> Dict[str, str]:
        body = """
        <p style="margin:0 0 16px;font-size:15px;line-height:1.6;color:#4b5563;">
          Your email is verified and your StockScope account is ready.
        </p>
        <div style="background:#f0fdf4;border:1px solid #bbf7d0;border-radius:10px;padding:16px 18px;margin:0 0 20px;">
          <p style="margin:0;font-size:14px;line-height:1.6;color:#166534;">
            You’re all set to track stocks, watchlists, and market sentiment in one place.
          </p>
        </div>
        <p style="margin:0;font-size:15px;line-height:1.6;color:#4b5563;">
          Log in anytime and start building your trading view. We’re glad you’re here.
        </p>
        """
        html = self._wrap_email("Welcome to StockScope", body)

        message = MessageSchema(
            subject="Welcome to StockScope — you’re verified",
            recipients=emails,
            body=html,
            subtype=MessageType.html,
        )
        await self._fm.send_message(message)
        return {"message": "Confirmation email sent"}
