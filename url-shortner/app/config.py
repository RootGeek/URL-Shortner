import os

class Settings:
    PROJECT_NAME: str = "RootGeek"
    SECRET_KEY: str = os.getenv("ROOTGEEK_SECRET_KEY", "change-this-secret-in-production")
    SESSION_COOKIE_NAME: str = "linkscope_session"
    DATABASE_URL: str = os.getenv("ROOTGEEK_DATABASE_URL", "sqlite:///./linkscope.db")

settings = Settings()
