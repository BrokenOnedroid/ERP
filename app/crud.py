from sqlalchemy.orm import Session
from app.database import SessionLocal
from sqlalchemy import insert 
from app.models import Article, Inventory
from app.database import engine, SessionLocal


def add_art_entry(db: Session):
    pass

def del_art_entry(db: Session):
    pass

def update_art_entry(db: Session):
    pass

def get_art_entry(db: Session):
    pass

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

    