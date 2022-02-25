from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String
from app.configs.database import db


@dataclass
class Leads(db.Model):
    name: str
    email: str
    phone: str
    creation_date: str
    last_visit: str
    visits: int

    __tablename__ = "Leads"

    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True, primary_key=True)
    phone = Column(String, unique=True, nullable=False)
    creation_date = Column(DateTime, default=datetime.now())
    last_visit = Column(DateTime, default=datetime.now())
    visits = Column(Integer, default=1)
