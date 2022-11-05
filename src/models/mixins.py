from src.db import db
from sqlalchemy import func


class Timestamp(object):
    updated_at = db.Column(db.DATETIME, default=func.now(), onupdate=func.now())
    created_at = db.Column(db.DATETIME, default=func.now())
