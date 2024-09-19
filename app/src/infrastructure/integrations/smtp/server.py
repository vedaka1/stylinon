import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP, SMTP_SSL

import aiosmtplib
from src.application.common.interfaces.smtp import (
    SMTPServerInterface,
    SyncSMTPServerInterface,
)
from src.domain.common.exceptions.base import ApplicationException
from src.infrastructure.settings import settings

logger = logging.getLogger()


class AsyncSMTPServer(SMTPServerInterface):

    def __init__(
        self,
        server: aiosmtplib.SMTP,
        from_address: str,
        password: str,
        subject: str,
    ) -> None:
        self.server = server
        self.from_address = from_address
        self.password = password
        self.subject = subject

    async def start(self) -> None:
        logger.info("Starting smtp server")
        await self.server.connect()

    def create_message(self, content: str, to_address: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["Subject"] = self.subject
        message["From"] = self.from_address
        message["To"] = to_address
        html = MIMEText(content, "html")
        message.attach(html)
        return message

    async def send_email(self, message: MIMEMultipart) -> None:
        try:
            await self.server.sendmail(
                self.from_address,
                message["To"],
                message.as_string(),
            )
        except Exception as e:
            logger.error(f"Error sending email: {e}")
        return None

    async def stop(self) -> None:
        logger.info("Stopping smtp server")
        await self.server.quit()

    async def check_connection(self) -> None:
        if self.server.is_connected == False:
            if self.server._connect_lock and self.server._connect_lock.locked():
                self.server.close()
            try:
                logger.info(f"Connecting SMTP server.")
                await self.server.connect()
            except Exception as e:
                logger.error(f"Error connecting to SMTP server: {e}")
                raise ApplicationException


class SyncSMTPServer(SyncSMTPServerInterface):
    def __init__(
        self,
        from_address: str,
        password: str,
        subject: str,
    ) -> None:
        self.from_address = from_address
        self.password = password
        self.subject = subject

    def create_message(self, content: str, to_address: str) -> MIMEMultipart:
        message = MIMEMultipart()
        message["Subject"] = self.subject
        message["From"] = self.from_address
        message["To"] = to_address
        html = MIMEText(content, "html")
        message.attach(html)
        return message

    def _send(self, message: MIMEMultipart) -> None:
        with SMTP_SSL(settings.smtp.HOST, settings.smtp.PORT) as server:
            server.login(settings.smtp.FROM_EMAIL, settings.smtp.PASSWORD)
            try:
                response = server.sendmail(
                    settings.smtp.FROM_EMAIL,
                    message["To"],
                    message.as_string(),
                )
                print(response)
            except Exception as e:
                logger.error(f"Error while sending email: {e}")
                raise ApplicationException

    async def send_email(self, message: MIMEMultipart) -> None:
        with ThreadPoolExecutor(max_workers=5) as executor:
            await asyncio.get_event_loop().run_in_executor(
                executor,
                self._send,
                message,
            )
        return None
