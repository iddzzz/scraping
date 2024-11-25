from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Url, Listing


DATABASE_URL = "sqlite:///./streeteasy.db"

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
