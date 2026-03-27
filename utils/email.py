import os
import asyncio
import resend
from config import FRONTEND_URL

resend.api_key = os.getenv("RESEND_API_KEY", "")
MAIL_FROM = os.getenv("MAIL_FROM", "noreply@verify.daia.do")


async def send_verification_email(email: str, code: str, purpose: str = "verify"):
    if purpose == "verify":
        verify_link = f"{FRONTEND_URL}/verify?email={email}&code={code}"
    elif purpose == "change_email":
        verify_link = f"{FRONTEND_URL}/verify-email-change?email={email}&code={code}"
    else:
        verify_link = f"{FRONTEND_URL}/verify?email={email}&code={code}"

    html_content = f"""
    <html>
        <body style="font-family:sans-serif;max-width:480px;margin:0 auto;padding:32px 16px;">
            <h2 style="margin-bottom:8px;">Email Verification</h2>
            <p>Your verification code is:</p>
            <h1 style="letter-spacing:8px;font-size:40px;margin:16px 0;">{code}</h1>
            <p>Or click the button below:</p>
            <a href="{verify_link}"
               style="display:inline-block;padding:12px 24px;background-color:#2563eb;
                      color:white;text-decoration:none;border-radius:6px;font-weight:600;">
               Verify Email
            </a>
            <p style="margin-top:24px;color:#6b7280;font-size:14px;">
                If the button doesn't work, copy and paste this link:<br/>
                <a href="{verify_link}" style="color:#2563eb;">{verify_link}</a>
            </p>
            <p style="color:#6b7280;font-size:12px;">This code expires in 10 minutes.</p>
        </body>
    </html>
    """

    params: resend.Emails.SendParams = {
        "from": MAIL_FROM,
        "to": [email],
        "subject": "Verify your account",
        "html": html_content,
    }

    await asyncio.to_thread(resend.Emails.send, params)


async def send_password_reset_email(email: str, token: str):
    reset_link = f"{FRONTEND_URL}/reset-password?token={token}"

    html_content = f"""
    <html>
        <body style="font-family:sans-serif;max-width:480px;margin:0 auto;padding:32px 16px;">
            <h2 style="margin-bottom:8px;">Reset Your Password</h2>
            <p>We received a request to reset your password. Click the button below to choose a new one:</p>
            <a href="{reset_link}"
               style="display:inline-block;padding:12px 24px;background-color:#2563eb;
                      color:white;text-decoration:none;border-radius:6px;font-weight:600;">
               Reset Password
            </a>
            <p style="margin-top:24px;color:#6b7280;font-size:14px;">
                If the button doesn't work, copy and paste this link:<br/>
                <a href="{reset_link}" style="color:#2563eb;">{reset_link}</a>
            </p>
            <p style="color:#6b7280;font-size:12px;">This link expires in 15 minutes. If you didn't request this, you can ignore this email.</p>
        </body>
    </html>
    """

    params: resend.Emails.SendParams = {
        "from": MAIL_FROM,
        "to": [email],
        "subject": "Reset your DAIA password",
        "html": html_content,
    }

    await asyncio.to_thread(resend.Emails.send, params)
