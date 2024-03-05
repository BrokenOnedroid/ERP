#database table definitionsnow

from sqlalchemy import Boolean, Column, Integer, String, DateTime, ForeignKey, nvarchar
from sqlalchemy.sql import func

from sqlalchemy.orm import relationship

# Base comes of database.py
from app.database import Base

class Article(Base):
    """
    Model for the article table.
    """
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, index=True)                          
    article_number = Column(nvarchar(18), nullable=False)
    name = Column(String(80))
    purchase_price = Column(float, default=0.0)
    purchase_price = Column(float, default=0.0)
    ts = Column(DateTime(timezone=True), server_default=func.now())             # timestamp 
    ts_last_change = Column(DateTime(timezone=True), server_default=func.now()) 

class Inventory(Base):
    """
    Model for the Inventory table.
    """
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)                      
    article_number = Column(nvarchar(18), nullable=False)      
    location = Column(String(20), default='NaN')   
    stock = Column(float, default=0.0)                                             