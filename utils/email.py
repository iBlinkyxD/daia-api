import os
import resend
from config import FRONTEND_URL

resend.api_key = os.getenv("RESEND_API_KEY")


async def send_verification_email(email: str, code: str):

    verify_link = f"{FRONTEND_URL}/verify?email={email}&code={code}"

    html_content = f"""
    <html>
        <body>
            <h2>Verify Your Account</h2>

            <p>Your verification code is:</p>

            <h1 style="letter-spacing:4px;">{code}</h1>

            <p>Or click the button below to verify instantly:</p>

            <a href="{verify_link}"
               style="
               display:inline-block;
               padding:12px 20px;
               background-color:#2563eb;
               color:white;
               text-decoration:none;
               border-radius:6px;">
               Verify Account
            </a>

            <p style="margin-top:20px;">
                If the button doesn't work, copy this link:
            </p>

            <p>{verify_link}</p>

        </body>
    </html>
    """

    response = resend.Emails.send({
        "from": os.getenv("RESEND_FROM", "onboarding@resend.dev"),
        "to": [email],
        "subject": "Verify your account",
        "html": html_content
    })

    return response