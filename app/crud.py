from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import insert, delete 
from app.models import Article, Inventory
from app.database import engine, SessionLocal
from app.schemas import ArtCreate

def add_art_entry(art: ArtCreate):
    with engine.connect() as db:
        insert_stmt = insert(Article).values(article_number=art.art_number, name=art.art_name, additional_information=art.art_info, purchase_price=art.ek, selling_price=art.vk, producer=art.producer)
        db.execute(insert_stmt)
        db.commit()

def del_art_entry(art_id : int) -> int:
    with engine.connect() as db:
        delete_stmt = delete(Article).where(Article.id == art_id)
        db.execute(delete_stmt)
        db.commit()

            

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