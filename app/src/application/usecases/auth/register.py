import logging
from dataclasses import dataclass

from src.application.common.password_hasher import PasswordHasherInterface
from src.application.common.transaction import TransactionManagerInterface
from src.application.contracts.commands.user import RegisterCommand
from src.domain.users.entities import User
from src.domain.users.service import UserServiceInterface

logger = logging.getLogger()


@dataclass
class RegisterUseCase:
    user_service: UserServiceInterface
    password_hasher: PasswordHasherInterface
    transaction_manager: TransactionManagerInterface

    async def execute(self, command: RegisterCommand) -> None:
        hashed_password = self.password_hasher.hash(command.password)
        user = User.create(
            email=command.email,
            hashed_password=hashed_password,
            mobile_phone=command.mobile_phone,
            first_name=command.first_name,
            last_name=command.last_name,
        )
        await self.user_service.create(user)
        # user_confirmation = UserConfirmation.create(user_id=user.id)
        # await self.user_confirmation_repository.create(user_confirmation)
        # event = NewUserRegistered(
        #     email=user.email,
        #     message_text="Here is the link to confirm your account<br>",
        #     confirmation_link="<a href='http://localhost/api/v1/auth/confirmation?id={0}&code={1}'>Confirm</a>".format(
        #         user_confirmation.id, user_confirmation.code
        #     ),
        # )
        # try:
        #     await self.message_broker.send_message(
        #         topic=self.broker_topic,
        #         value=convert_event_to_broker_message(event),
        #         key=str(event.id).encode(),
        #     )
        # except Exception as e:
        #     logger.error("Failed to send message to broker: {0}".format(e))

        await self.transaction_manager.commit()
        return None
