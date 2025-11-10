import secrets
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.hash import bcrypt

from .config import settings
from .database import Base, engine, SessionLocal
from .models import User
from .auth import router as auth_router
from .routers.dashboard import router as dashboard_router
from .routers.links import router as links_router


def init_db():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        user_count = db.query(User).count()
        if user_count == 0:
            password = "".join(secrets.choice("ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789") for _ in range(16))
            user = User(username="admin", password_hash=bcrypt.hash(password))
            db.add(user)
            db.commit()
            print("\n[RootGeek] Initial admin created:")
            print(f"  Username: admin")
            print(f"  Password: {password}\n")
    finally:
        db.close()


def create_app() -> FastAPI:
    app = FastAPI(title=settings.PROJECT_NAME)

    # Static files
    app.mount("/static", StaticFiles(directory="app/static"), name="static")

    # CORS (loose for demo, tighten in prod)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routers
    app.include_router(auth_router)
    app.include_router(dashboard_router)
    app.include_router(links_router)

    @app.on_event("startup")
    def on_startup():
        init_db()

    return app


app = create_app()
