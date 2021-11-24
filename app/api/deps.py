"""Authorization management"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError

from core.config import settings
from db import db_users
from schemas import schemas


# Utility function to authenticate.
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/login/access-token",
)


def get_db():
    """Return the users database."""
    users_db = db_users.users
    return users_db


def get_user(db, username: str):
    """Get the users data from the database.

    Parameters
    ----------
    db : dict
        A database in dict format.
    username : str
        The user username.

    Return
    ------
    UserInDB : The user's data for the specified username.
    """
    if username in db:
        user_dict = db[username]
        return schemas.UserInDB(**user_dict)


def get_current_user(db = Depends(get_db), token: str = Depends(oauth2_scheme)):
    """Get the current user after verifying the token authorization.

    Parameters
    ----------
    db : dict
        A database in dict format.
    token : str
        The token that was created for the user.

    Raises
    ------
    HTTPException : 401
        Not enough permissions if attempting to access an endpoint
        without the correct authorization.
    HTTPException : 403
        Could not validate credentials if token decoding fails,
        the data is not valid with the model or there is no username.

    Return
    ------
    user : UserInDB : The user's data for the specified username.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        token_data = schemas.TokenData(username=username)
    except (JWTError, ValidationError):
        raise credentials_exception
    user = get_user(db, username=token_data.username)
    if not user:
        raise credentials_exception
    return user


def get_current_admin_user(current_user: schemas.User = Depends(get_current_user)):
    """Get the current user with admin rights.

    Parameter
    ---------
    current_user : UserInDB
        The user's data for the specified username.

    Raise
    -----
    HTTPException : 401
        Not enough permissions if attempting to access an endpoint
        without the correct authorization.
    HTTPException : 403
        Not authorized if the user does not have the admin rights.
    
    Return
    ------
    current_user : UserInDB
        The user's data for the specified username.
    """
    if not current_user.admin:
        raise HTTPException(
            status_code=403, 
            detail="The user doesn't have enough privileges",
        )
    return current_user
