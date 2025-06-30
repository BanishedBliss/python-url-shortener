from sqlalchemy import Column, String
from .database import Base


class URLMapping(Base):
    __tablename__ = "url_mappings"

    short_id = Column(String(8), primary_key=True, index=True)
    original_url = Column(String(2048), nullable=False)