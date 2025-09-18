import logging
from uuid import uuid4
from fastapi import APIRouter, Response, status, HTTPException

from .dependencies import UserCollectionDep, SessionCollectionDep

from .schemas import UserCreated, UserOut, UserInputForm, UserLoginForm
from .utils import Hasher

router = APIRouter(prefix="/users", tags=["devices"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=UserCreated, status_code=status.HTTP_201_CREATED)
def create_user(user: UserInputForm, collection: UserCollectionDep):
    newUser = user.model_dump()
    hashed_password = Hasher.get_password_hash(user.password)
    newUser["password"] = hashed_password

    try:
        collection.insert_one(newUser)
    except Exception as e:
        logger.info(f"Failed to insert new user: {e}")
        raise HTTPException(status_code=400, detail="Unable to create user")

    return user


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: str, collection: UserCollectionDep):
    try:
        logger.info(f"Fetching user with id: {user_id}")
        user = collection.find_one({"id": user_id})
    except Exception as e:
        logger.info(f"Failed to insert new user: {e}")
        raise HTTPException(status_code=400, detail="Unable to create user")

    return user


@router.post("/login", status_code=status.HTTP_200_OK)
def create_session(
    user_data: UserLoginForm,
    users_collection: UserCollectionDep,
    session_collection: SessionCollectionDep,
    response: Response,
):
    try:
        user = users_collection.find_one({"username": user_data.username})

        if not user:
            raise ValueError("Invalid credentials")

        logger.info(f"To be compared: {user_data.password} with {user['password']}")
        password_valid = Hasher.verify_password(user_data.password, user["password"])
        logger.info(f"Password valid: {password_valid}")

        if not password_valid:
            raise ValueError("Invalid credentials")

        session_id = uuid4().hex

        session_collection.insert_one(
            {"user_id": user["_id"], "session_id": session_id}
        )
        session_collection.find_one_and_delete({"user_id": user["_id"]})

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
        logger.info(f"Failed to create session: {e}")
        raise HTTPException(status_code=400, detail="Unable to create session")

    return
