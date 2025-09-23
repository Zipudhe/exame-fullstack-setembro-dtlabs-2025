import logging
from uuid import uuid4
from fastapi import APIRouter, Response, status, HTTPException

from .dependencies import UserCollectionDep
from src.schemas import RedisDep

from .schemas import UserOutPut, GetUser, UserInputForm, UserLoginForm
from .utils import Hasher

router = APIRouter(prefix="/users", tags=["devices"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserOutPut, status_code=status.HTTP_201_CREATED)
def create_user(user: UserInputForm, collection: UserCollectionDep):
    newUser = user.model_dump()
    hashed_password = Hasher.get_password_hash(user.password)
    newUser["password"] = hashed_password

    try:
        collection.insert_one(newUser)
    except Exception as e:
        logger.debug(f"Failed to insert new user: {e}")
        raise HTTPException(status_code=400, detail="Unable to create user")

    return user


@router.get("/{user_id}", response_model=GetUser)
def get_user(user_id: str, collection: UserCollectionDep):
    try:
        user = collection.find_one({"id": user_id})
    except Exception as e:
        logger.debug(f"Failed to insert new user: {e}")
        raise HTTPException(status_code=400, detail="Unable to create user")

    return user


@router.post("/login", status_code=status.HTTP_200_OK)
def create_session(
    user_data: UserLoginForm,
    users_collection: UserCollectionDep,
    redis_client: RedisDep,
    response: Response,
):
    try:
        user = users_collection.find_one({"username": user_data.username})

        if not user:
            raise ValueError("Invalid credentials")

        password_valid = Hasher.verify_password(user_data.password, user["password"])

        if not password_valid:
            raise ValueError("Invalid credentials")

        session_id = uuid4().hex
        redis_client.setex(f"userSession:{session_id}", 3600, user["id"])

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=False,
            samesite="none",
            expires=3600,
            max_age=3600,
        )

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception as e:
        logger.debug(f"Failed to create session: {e}")
        raise HTTPException(status_code=400, detail="Unable to create session")

    return
