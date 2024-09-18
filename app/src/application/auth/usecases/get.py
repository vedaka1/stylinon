# from dataclasses import dataclass

# from src.application.auth.service import AuthServiceInterface
# from src.application.users.commands import GetUserBySessionCommand
# from src.application.users.responses import UserOut


# @dataclass
# class GetUserBySessionUseCase:
#     auth_service: AuthServiceInterface

#     async def execute(self, command: GetUserBySessionCommand) -> UserOut:
#         user = await self.auth_service.get_by_session_id(session_id=command.session_id)
#         user_out = UserOut(
#             id=str(user.id),
#             email=user.email,
#             mobile_phone=user.mobile_phone,
#             first_name=user.first_name,
#             last_name=user.last_name,
#             is_verified=user.is_verified,
#             role=user.role,
#         )
#         return user_out
