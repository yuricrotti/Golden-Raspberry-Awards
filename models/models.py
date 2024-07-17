from sqlalchemy import Column, Integer, String, Boolean

from database.database import Base

class Award(Base):
    __tablename__ = "awards"

    id: int = Column(Integer, primary_key=True, index=True)
    year = Column(Integer)
    title = Column(String)
    studios = Column(String)
    producers = Column(String)
    winner = Column(Boolean, default=False)