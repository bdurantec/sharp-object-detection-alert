import os
import smtplib
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from src.domain.model.email_html_content import EmailHtmlContent


class GmailSMTP:
    def __init__(self, recipient: str):
        self.__recipient: str = recipient
        self.__sender: str = os.getenv('GMAIL_SMTP_SENDER')
        self.__password: str = os.getenv('GMAIL_SMTP_PASSWORD')
        self.__server: str = os.getenv('GMAIL_SMTP_SERVER', 'smtp.gmail.com')
        self.__port: int = os.getenv('GMAIL_SMTP_PORT', 587)

    def send_email(self, email_content: EmailHtmlContent):
        msg = MIMEMultipart()
        msg["From"] = self.__sender
        msg["To"] = self.__recipient
        msg["Subject"] = email_content.subject

        msg.attach(MIMEText(email_content.html_code, "html"))

        for i, image in enumerate(email_content.list_image_analysis):
            try:
                if isinstance(image.image_stream, bytes):
                    image_bytes = image.image_stream
                else:
                    with open(image.image_stream, "rb") as img_file:
                        image_bytes = img_file.read()

                mime = MIMEBase("image", "jpeg")
                mime.set_payload(image_bytes)
                encoders.encode_base64(mime)
                mime.add_header("Content-ID", f"<imagem_{i}>")
                mime.add_header("Content-Disposition", "inline", filename=f"imagem_{i}.jpg")
                msg.attach(mime)
            except Exception as e:
                print(f"Error attaching image {image.image_stream} to MIME: {e}")
                raise

        try:
            with smtplib.SMTP(self.__server, self.__port) as server:
                server.starttls()
                server.login(self.__sender, self.__password)
                server.sendmail(self.__sender, self.__recipient, msg.as_string())
                print(f"Email sent successfully to {self.__recipient}!")
        except Exception as e:
            print(f"Error sending email: {e}")
            raise
