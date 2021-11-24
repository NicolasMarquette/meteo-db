"""The login endpoint."""

from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm

from api import deps
from core import security
from core.config import settings
from schemas import schemas


router = APIRouter()


@router.post("/login/access-token", response_model=schemas.Token)
async def login_for_access_token(
    db_session: dict = Depends(deps.get_db_session),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """Give a token for the authorization.
    \f
    Parameter
    ---------
    db_session : dict
        A database in dict format.
    form_data : OAuth2PasswordRequestForm
        The authorization request form.

    Raise
    -----
    HTTPException : 400
        If the username or the password input is not correct.

    Return
    ------
    dict : A dictionnary with the token and the type of token.
    """
    user = security.authenticate_user(
        db_session, username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
