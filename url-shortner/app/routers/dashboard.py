from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import Link, Click
from ..auth import require_user

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/")
def root():
    return RedirectResponse(url="/dashboard")


@router.get("/dashboard")
def dashboard(request: Request, db: Session = Depends(get_db), user=Depends(require_user)):
    total_links = db.query(func.count(Link.id)).scalar() or 0
    total_clicks = db.query(func.count(Click.id)).scalar() or 0

    today = datetime.utcnow().date()
    day_start = datetime.combine(today, datetime.min.time())
    clicks_today = db.query(func.count(Click.id)).filter(Click.timestamp >= day_start).scalar() or 0

    unique_ips = db.query(Click.ip_address).distinct().count()

    recent_clicks = (
        db.query(Click)
        .order_by(Click.timestamp.desc())
        .limit(10)
        .all()
    )

    clicks_last_7_days = (
        db.query(
            func.date(Click.timestamp).label("day"),
            func.count(Click.id).label("count")
        )
        .filter(Click.timestamp >= datetime.utcnow() - timedelta(days=7))
        .group_by(func.date(Click.timestamp))
        .order_by("day")
        .all()
    )

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "user": user,
            "total_links": total_links,
            "total_clicks": total_clicks,
            "clicks_today": clicks_today,
            "unique_ips": unique_ips,
            "recent_clicks": recent_clicks,
            "clicks_last_7_days": clicks_last_7_days,
        },
    )
