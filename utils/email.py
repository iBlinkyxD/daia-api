import os
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from config import FRONTEND_URL

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("MAIL_USERNAME"),
    MAIL_PASSWORD=os.getenv("MAIL_PASSWORD"),
    MAIL_FROM=os.getenv("MAIL_FROM"),
    MAIL_PORT=587,
    MAIL_SERVER="smtp.gmail.com",
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)

async def send_verification_email(email: str, code: str, purpose: str = "verify"):

    if purpose == "verify":
        verify_link = f"https://daia-landing.netlify.app/verify?email={email}&code={code}"

    elif purpose == "change_email":
        verify_link = f"https://daia-landing.netlify.app/verify-email-change?email={email}&code={code}"

    html_content = f"""
    <html>
        <body>
            <h2>Email Verification</h2>

            <p>Your verification code is:</p>

            <h1 style="letter-spacing:4px;">{code}</h1>

            <p>Or click the button below:</p>

            <a href="{verify_link}"
               style="
               display:inline-block;
               padding:12px 20px;
               background-color:#2563eb;
               color:white;
               text-decoration:none;
               border-radius:6px;">
               Verify
            </a>

            <p>If the button doesn't work:</p>
            <p>{verify_link}</p>

        </body>
    </html>
    """

    message = MessageSchema(
        subject="Verify your account",
        recipients=[email],
        body=html_content,
        subtype="html"
    )

    fm = FastMail(conf)
    await fm.send_message(message)