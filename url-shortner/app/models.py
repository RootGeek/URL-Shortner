from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(64), unique=True, index=True, nullable=False)
    target_url = Column(String(2048), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    created_by_id = Column(Integer, ForeignKey("users.id"))
    tags = Column(String(255), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    max_clicks = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)

    created_by = relationship("User")
    clicks = relationship("Click", back_populates="link", cascade="all, delete-orphan")

class Click(Base):
    __tablename__ = "clicks"

    id = Column(Integer, primary_key=True, index=True)
    link_id = Column(Integer, ForeignKey("links.id"), nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    ip_address = Column(String(64))
    user_agent = Column(String(512))
    client_type = Column(String(64))
    referrer = Column(String(512))
    accept_language = Column(String(128))

    link = relationship("Link", back_populates="clicks")
