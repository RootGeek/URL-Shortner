from datetime import timedelta, datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request, Response
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from itsdangerous import Signer, BadSignature

from .config import settings
from .database import get_db
from .models import User

router = APIRouter()

signer = Signer(settings.SECRET_KEY)

SESSION_MAX_AGE = 60 * 60 * 8  # 8 hours


def create_session_token(user_id: int) -> str:
    payload = f"{user_id}:{int(datetime.utcnow().timestamp())}"
    return signer.sign(payload.encode()).decode()


def decode_session_token(token: str) -> Optional[int]:
    try:
        data = signer.unsign(token.encode()).decode()
        user_id_str, ts_str = data.split(":")
        ts = int(ts_str)
        if int(datetime.utcnow().timestamp()) - ts > SESSION_MAX_AGE:
            return None
        return int(user_id_str)
    except (BadSignature, ValueError):
        return None


def get_current_user(request: Request, db: Session = Depends(get_db)) -> Optional[User]:
    token = request.cookies.get(settings.SESSION_COOKIE_NAME)
    if not token:
        return None
    user_id = decode_session_token(token)
    if not user_id:
        return None
    return db.query(User).filter(User.id == user_id).first()


def require_user(user: User = Depends(get_current_user)) -> User:
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return user


@router.get("/login")
def login_page(request: Request):
    from fastapi.templating import Jinja2Templates
    templates = Jinja2Templates(directory="app/templates")
    return templates.TemplateResponse("auth_login.html", {"request": request})


@router.post("/login")
def login(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.username == username).first()
    if not user or not bcrypt.verify(password, user.password_hash):
        from fastapi.templating import Jinja2Templates
        templates = Jinja2Templates(directory="app/templates")
        return templates.TemplateResponse(
            "auth_login.html",
            {"request": request, "error": "Invalid credentials."},
            status_code=401,
        )

    token = create_session_token(user.id)
    resp = RedirectResponse(url="/dashboard", status_code=303)
    resp.set_cookie(
        key=settings.SESSION_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=False,  # Set to True when behind HTTPS
        samesite="lax",
        max_age=SESSION_MAX_AGE,
    )
    return resp


@router.get("/logout")
def logout():
    resp = RedirectResponse(url="/login", status_code=303)
    resp.delete_cookie(settings.SESSION_COOKIE_NAME)
    return resp
