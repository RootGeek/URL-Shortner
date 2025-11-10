import re
import secrets
from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from user_agents import parse as parse_ua

from ..database import get_db
from ..models import Link, Click
from ..auth import require_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

SLUG_REGEX = re.compile(r"^[a-zA-Z0-9-_]+$")


def generate_slug(db: Session, length: int = 7) -> str:
    alphabet = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    while True:
        slug = "".join(secrets.choice(alphabet) for _ in range(length))
        if not db.query(Link).filter_by(slug=slug).first():
            return slug


@router.get("/links")
def list_links(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    links = db.query(Link).order_by(Link.created_at.desc()).all()
    return templates.TemplateResponse(
        "links.html",
        {"request": request, "user": user, "links": links},
    )


@router.get("/links/create")
def create_link_page(request: Request, user=Depends(require_user)):
    return templates.TemplateResponse(
        "create_link.html",
        {"request": request, "user": user},
    )


@router.post("/links/create")
def create_link(
    request: Request,
    db: Session = Depends(get_db),
    user=Depends(require_user),
    target_url: str = Form(...),
    slug: Optional[str] = Form(None),
    tags: Optional[str] = Form(None),
    expires_at: Optional[str] = Form(None),
    max_clicks: Optional[str] = Form(None),
):
    target_url = target_url.strip()
    if not (target_url.startswith("http://") or target_url.startswith("https://")):
        target_url = "http://" + target_url

    if slug:
        slug = slug.strip()
        if not SLUG_REGEX.match(slug):
            raise HTTPException(status_code=400, detail="Invalid slug format.")
        if db.query(Link).filter_by(slug=slug).first():
            raise HTTPException(status_code=400, detail="Slug already in use.")
    else:
        slug = generate_slug(db)

    expires_at_dt = None
    if expires_at:
        try:
            expires_at_dt = datetime.fromisoformat(expires_at)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid expiration date.")


    max_clicks_value = None
    if max_clicks is not None and str(max_clicks).strip() != "":
        try:
            mc_int = int(str(max_clicks).strip())
            if mc_int > 0:
                max_clicks_value = mc_int
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid max clicks value.")

    link = Link(
        slug=slug,
        target_url=target_url,
        created_by_id=user.id,
        tags=tags,
        expires_at=expires_at_dt,
        max_clicks=max_clicks_value,
        is_active=True,
    )
    db.add(link)
    db.commit()
    db.refresh(link)

    return RedirectResponse(url=f"/links/{link.id}", status_code=303)


@router.get("/links/{link_id}")
def link_detail(link_id: int, request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    link = db.query(Link).filter_by(id=link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    clicks = (
        db.query(Click)
        .filter(Click.link_id == link.id)
        .order_by(Click.timestamp.desc())
        .all()
    )
    return templates.TemplateResponse(
        "link_detail.html",
        {"request": request, "user": user, "link": link, "clicks": clicks},
    )



@router.post("/links/{link_id}/delete")
def delete_link(link_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    link = db.query(Link).filter_by(id=link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    db.delete(link)
    db.commit()
    return RedirectResponse(url="/links", status_code=303)


@router.get("/api/links/{link_id}/clicks-count")
def api_link_clicks_count(link_id: int, db: Session = Depends(get_db), user=Depends(require_user)):
    link = db.query(Link).filter_by(id=link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")
    count = db.query(Click).filter(Click.link_id == link.id).count()
    return {"clicks": count}

@router.get("/r/{slug}")
def redirect_slug(slug: str, request: Request, db: Session = Depends(get_db)):
    link = db.query(Link).filter_by(slug=slug).first()
    if not link or not link.is_active:
        raise HTTPException(status_code=404, detail="Link not found")

    # Handle expiration
    if link.expires_at and datetime.utcnow() > link.expires_at:
        link.is_active = False
        db.commit()
        raise HTTPException(status_code=410, detail="Link expired")

    # Handle max clicks
    if link.max_clicks is not None:
        click_count = db.query(Click).filter(Click.link_id == link.id).count()
        if click_count >= link.max_clicks:
            link.is_active = False
            db.commit()
            raise HTTPException(status_code=410, detail="Link click limit reached")

    client_host = request.client.host if request.client else "unknown"
    ua_string = request.headers.get("User-Agent", "")
    referrer = request.headers.get("referer", "")
    accept_language = request.headers.get("accept-language", "")

    ua = parse_ua(ua_string)
    if ua.is_mobile:
        client_type = "Mobile"
    elif ua.is_tablet:
        client_type = "Tablet"
    elif ua.is_pc:
        client_type = "Desktop"
    elif ua.is_bot:
        client_type = "Bot"
    else:
        client_type = "Unknown"

    click = Click(
        link_id=link.id,
        ip_address=client_host,
        user_agent=ua_string[:500],
        client_type=client_type,
        referrer=referrer[:500],
        accept_language=accept_language[:120],
    )
    db.add(click)
    db.commit()

    return RedirectResponse(url=link.target_url, status_code=307)
