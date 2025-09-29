import logging
from uuid import uuid4
from fastapi import APIRouter, Response, status, HTTPException, Request

from .dependencies import UserCollectionDep
from config.env_vars import get_enviroment
from src.schemas import RedisDep

from .schemas import UserOutPut, GetUser, UserInputForm, UserLoginForm
from .utils import Hasher

router = APIRouter(prefix="/users", tags=["users"])
logger = logging.getLogger(__name__)
enviroment = get_enviroment()


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


@router.post("/auth", status_code=status.HTTP_204_NO_CONTENT)
def auth_user(request: Request):
    session = request.cookies.get("session_id")

    if not session:
        raise HTTPException(status_code=401, detail="Unauthorized")

    return {"message": "Authorized"}


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
    logger.debug(f"Attempting login for user: {user_data.email}")
    try:
        user = users_collection.find_one({"email": user_data.email})
        print(f"user: {user}")

        if not user:
            logger.debug("user not found")
            raise ValueError("Invalid credentials")

        logger.info(f"username: {user['username']} \t password: {user['password']}")
        password_valid = Hasher.verify_password(user_data.password, user["password"])

        if not password_valid:
            raise ValueError("Invalid credentials")

        session_id = uuid4().hex
        redis_client.setex(f"userSession:{session_id}", 3600, user["id"])

        response.set_cookie(
            key="session_id",
            value=session_id,
            httponly=True,
            secure=False if enviroment == "development" else True,
            samesite="lax",
            expires=3600,
            max_age=3600,
        )

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception as e:
        logger.debug(f"Failed to create session: {e}")
        raise HTTPException(status_code=400, detail="Unable to create session")

    return


@router.delete("/logout", status_code=status.HTTP_200_OK)
def delete_session(
    request: Request,
    users_collection: UserCollectionDep,
    response: Response,
    redis_client: RedisDep,
):
    user_id = request.cookies.get("session_id")
    user_session = f"userSession:{user_id}"

    try:
        user = users_collection.find_one({"id": user_session})

        if not user:
            raise ValueError("Invalid credentials")

        redis_client.delete(user_session)
        response.delete_cookie(key="session_id")

    except ValueError as e:
        raise HTTPException(status_code=401, detail=str(e))

    except Exception as e:
        logger.debug(f"Failed to remove session: {e}")
        raise HTTPException(status_code=400, detail="Unable to delete session")

    return
