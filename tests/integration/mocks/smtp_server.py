from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

from src.application.common.interfaces.smtp import SyncSMTPServerInterface


class MockSyncSMTPServer(SyncSMTPServerInterface):

    def create_message(
        self,
        content: str,
        sender_name: str,
        to_address: str,
        subject: str,
    ) -> MIMEMultipart:
        message = MIMEMultipart()

        message["Subject"] = subject

        message["From"] = formataddr(
            (str(Header(sender_name, "utf-8")), "test@test.com"),
        )

        message["To"] = to_address

        html = MIMEText(content, "html")

        message.attach(html)

        return message

    def _send(self, message: MIMEMultipart) -> None:
        return None

    async def send_email(self, message: MIMEMultipart) -> None:
        self._send(message)
        return None
