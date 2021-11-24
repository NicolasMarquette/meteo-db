"""Security and authorization management"""

from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext

from core.config import settings
from schemas import schemas


# Utility function to hash the password.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create an access token to authenticate.

    Parameter
    ---------
    data : dict
        The data with the entered username and scope.
    expires_delta : Optional[timedelta]
        Expiration time for the token. Default value = None.

    Return
    ------
    encode_jwt : str
        The data encoded to create a token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password, hashed_password):
    """Verify if the password received match the hashed_password in database.

    Parameters
    ----------
    plain_password : str
        The password received from the authentication form.
    hashed_password : str
        The hashed password stored in the database.

    Return
    ------
    bool : The resultat of the verification.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hash the password received.

    Parameter
    ---------
    password : str
        The password received from the authentication form.

    Return
    ------
    str : The password hashed.
    """
    return pwd_context.hash(password)


def get_user(db_session, username: str):
    """Get the users data from the database.

    Parameters
    ----------
    db_session : dict
        A database in dict format.
    username : str
        The user username.

    Return
    ------
    UserInDB_session : The user's data for the specified username.
    """
    if username in db_session:
        user_dict = db_session[username]
        return schemas.UserInDB(**user_dict)


def authenticate_user(db_session, username: str, password: str):
    """Authenticate the user by checking if their username exists
    and if the password matches.

    Parameters
    ----------
    db_session : dict
        A database in dict format.
    username : str
        The user username.
    password : str
        The user password.

    Return
    ------
    user : UserInDB_session : The user's data for the specified username.
    """
    user = get_user(db_session, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
