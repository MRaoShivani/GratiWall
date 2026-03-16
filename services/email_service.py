import os
import smtplib
from email.message import EmailMessage
from email.utils import make_msgid
from pathlib import Path


def send_gratitude_email(
    to_email: str,
    receiver_name: str,
    sender_name: str,
    sender_email: str,
    image_path: str
):
    """
    Sends a gratitude email with an embedded card image.
    """

    email_sender = os.getenv("GMAIL_USER")
    email_password = os.getenv("GMAIL_APP_PASSWORD")

    if not email_sender or not email_password:
        raise RuntimeError("Email credentials not configured")

    # Create email
    msg = EmailMessage()
    msg["From"] = email_sender
    msg["To"] = to_email
    
    if sender_email:
        msg["Cc"] = sender_email

    msg["Subject"] = f"A note of appreciation from {sender_name} 🎉"

    # Create Content-ID for inline image
    image_cid = make_msgid(domain="gratitudewall")

    # HTML body
    msg.set_content("Your email client does not support HTML.")

    msg.add_alternative(
        f"""
        <html>
            <body style="font-family: Arial, sans-serif; background-color: #f7f7f7; padding: 20px;">
                <p>Hi <strong>{receiver_name}</strong>,</p>

                <p>You’ve received a gratitude message:</p>

                <div style="margin: 20px 0;">
                    <img src="cid:{image_cid[1:-1]}" 
                         style="max-width: 100%; border-radius: 10px;" />
                </div>

                <p style="margin-top: 30px;">
                    Warm regards,<br/>
                    <strong>{sender_name}</strong>
                </p>

                <hr/>
                <small>This message was sent via the Digital Gratitude Wall</small>
            </body>
        </html>
        """,
        subtype="html"
    )

    # Attach image
    image_path = Path(image_path)

    if not image_path.exists():
        raise FileNotFoundError(f"Card image not found: {image_path}")

    with open(image_path, "rb") as img:
        msg.get_payload()[1].add_related(
            img.read(),
            maintype="image",
            subtype="png",
            cid=image_cid
        )

    recipients = [to_email]
    if sender_email:
        recipients.append(sender_email)


    # Send email
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(email_sender, email_password)
        #server.send_message(msg)
        server.send_message(msg, to_addrs=recipients)
        

