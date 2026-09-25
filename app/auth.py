from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError


SECRET_KEY = "my-secret-key-change-this"

ALGORITHM = "HS256"

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin@123"


security = HTTPBearer()


def create_token(username):

    payload = {
        "sub": username,
        "exp": datetime.now(timezone.utc)
        + timedelta(hours=2)
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token


def login(username, password):

    if (
        username != ADMIN_USERNAME
        or password != ADMIN_PASSWORD
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid admin credentials"
        )

    return create_token(username)


def get_current_admin(
    credentials: HTTPAuthorizationCredentials =
    Depends(security)
):

    try:

        token = credentials.credentials

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        username = payload.get("sub")

        if username != ADMIN_USERNAME:

            raise HTTPException(
                status_code=401,
                detail="Admin access required"
            )

        return username

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token"
        )