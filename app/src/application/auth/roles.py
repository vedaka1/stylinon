from src.domain.users.entities import UserRole

RESTRICTIONS = {
    UserRole.ADMIN.value: f"{UserRole.USER.value} {UserRole.MANAGER.value} {UserRole.ADMIN.value}",
    UserRole.MANAGER.value: f"{UserRole.MANAGER.value} {UserRole.USER.value}",
    UserRole.USER.value: f"{UserRole.USER.value}",
}


def get_role_restrictions(role: UserRole) -> str:
    restrictions = RESTRICTIONS.get(role.value)
    if not restrictions:
        raise ValueError(f"Restrictions not found for role {role.value}")
    return restrictions
