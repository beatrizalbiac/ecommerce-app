from sqlmodel import Session, SQLModel, create_engine
import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True, pool_pre_ping=True)

def create_db_and_tables():
    from app.models import users, products, orders, order_items
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session
