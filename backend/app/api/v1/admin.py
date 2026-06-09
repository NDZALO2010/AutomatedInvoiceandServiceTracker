from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps import require_roles
from app.models.user import User, UserRole

router = APIRouter()


@router.get("/dashboard")
def admin_dashboard(
    _admin: Annotated[User, Depends(require_roles(UserRole.ADMIN))],
) -> dict[str, str]:
    return {"message": "admin dashboard"}
