from fastapi import APIRouter, status

from schemas import UserIn, UserOut

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserIn):
    return {}


@router.post("/login")
def create_session():
    return
