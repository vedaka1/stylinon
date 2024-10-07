import logging
from abc import ABC, abstractmethod
from email.mime.multipart import MIMEMultipart

logger = logging.getLogger()


class SMTPServerInterface(ABC):

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    def create_message(self, content: str, to_address: str) -> MIMEMultipart: ...

    @abstractmethod
    async def send_email(self, message: MIMEMultipart) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...

    @abstractmethod
    async def check_connection(self) -> None: ...


class SyncSMTPServerInterface(ABC):

    @abstractmethod
    def create_message(
        self,
        content: str,
        sender_name: str,
        to_address: str,
        subject: str,
    ) -> MIMEMultipart: ...

    @abstractmethod
    def _send(self, message: MIMEMultipart) -> None: ...

    @abstractmethod
    async def send_email(self, message: MIMEMultipart) -> None: ...
