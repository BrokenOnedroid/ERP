from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import insert 
from app.models import Article, Inventory
from app.database import engine, SessionLocal
import app.schemas

def add_art_entry(art : str, name:str, info: str = '', ek: float = 0.0, vk: float = 0.0, producer: str = "Unbekannt"):
    with engine.connect() as db:
        insert_stmt = insert(Article).values(article_number=art, name=name, additional_information=info, purchase_price=ek, selling_price=vk, producer=producer)
        db.execute(insert_stmt)
        db.commit()

def del_art_entry(id: int) -> int:
    with engine.connect() as db:
        art : Article  = db.query(Article).filter(Article.id == id).first()
        #lager = db.query(Inventory).filter(Inventory.article_number == art.article_number).first()
        #if lager is None:        
        db.delete(art)
        db.commit()
        return art.id
        #    return Article.id, True
        #else:
        #    return art.id, False
            

def update_art_entry(db: Session):
    pass

def get_art_entry(db: Session):
    pass

def get_art_entries():
    # Create a session using SessionLocal
    articles = []
    session = SessionLocal()
    try:
        articles = session.query(Article).all()
    finally:
        # Make sure to close the session
        session.close()
        return articles

def add_inv_entry(db: Session):
    pass

def del_inv_entry(db: Session):
    pass

def update_inv_entry(db: Session):
    pass

def get_inv_entries():
    # Create a session using SessionLocal
    session = SessionLocal()
    try:
        # Query all inventory entries
        inventory = session.query(Inventory).all()
    finally:
        # Make sure to close the session
        session.close()
        return inventory

def add_test_data(art: str, name: str, loc: str, stock: float):
    with engine.connect() as db:
        insert_stmt = insert(Inventory).values(article_number=art, name=name, location=loc, stock=stock)
        db.execute(insert_stmt)
        db.commit()