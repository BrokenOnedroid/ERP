#database table definitionsnow
from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.orm import mapped_column

from sqlalchemy import Float, Integer, String, DateTime, ForeignKey
from sqlalchemy.sql import func

# Base comes of database.py
from app.database import Base

class Base(DeclarativeBase):
    pass

class Article(Base):
    """
    Model for the article table.
    """
    __tablename__ = "article"

    id = mapped_column(Integer, primary_key=True, index=True)                          
    article_number = mapped_column(String(18), nullable=False)
    name = mapped_column(String(80))
    additional_information = mapped_column(String(420))    
    purchase_price = mapped_column(Float, default=0.0)
    selling_price = mapped_column(Float, default=0.0)
    ts = mapped_column(DateTime(timezone=True), server_default=func.now())             # timestamp 
    ts_last_change = mapped_column(DateTime(timezone=True), server_default=func.now()) 

class Inventory(Base):
    """
    Model for the Inventory table.
    """
    __tablename__ = "inventory"

    id = mapped_column(Integer, primary_key=True, index=True)                      
    article_number = mapped_column(String(18), ForeignKey('article.article_number'), nullable=False)
    name = mapped_column(String(80))      
    location = mapped_column(String(20), default='NaN')   
    stock = mapped_column(Float, default=0.0)
    
    # Establish relationship with the Article table
    article = relationship("Article", backref="inventory")                                             