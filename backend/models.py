from sqlalchemy import Column, Integer, String
from database import Base

class Listings(Base):
    __tablename__ = 'listings'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    type = Column(String)
    description = Column(String)
    location = Column(String)
    salary = Column(String)
    companyName = Column(String)
    companyDescription = Column(String)
    contactEmail = Column(String)
    contactPhone = Column(String)
