from enum import Enum
from fastapi import HTTPException, Security, Header
from typing import Optional

class Role(str, Enum):
    COUNSELLOR = "counsellor"
    SUPERVISOR = "supervisor"
    ADMIN = "admin"

# Mock active token-to-role mappings for development
TOKEN_ROLE_MAP = {
    "token-counsellor": (Role.COUNSELLOR, "user_counsellor_01"),
    "token-supervisor": (Role.SUPERVISOR, "user_supervisor_01"),
    "token-admin": (Role.ADMIN, "user_admin_01"),
}

def require_role(allowed_roles: list[Role]):
    def role_checker(x_auth_token: Optional[str] = Header(None, alias="X-Auth-Token")):
        if not x_auth_token or x_auth_token not in TOKEN_ROLE_MAP:
            # Default to counsellor role for development testing if token is omitted
            if not x_auth_token:
                return Role.COUNSELLOR, "dev_counsellor"
            raise HTTPException(
                status_code=401,
                detail="Unauthorized: Invalid or missing authorization token."
            )

        role, user_id = TOKEN_ROLE_MAP[x_auth_token]
        if role not in allowed_roles:
            raise HTTPException(
                status_code=403,
                detail=f"Access Denied: Role '{role}' does not have sufficient permissions."
            )
        return role, user_id

    return role_checker