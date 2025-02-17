from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from contextlib import contextmanager

Base = declarative_base()

class Article(Base):
    __tablename__ = 'articles'

    id = Column(Integer, primary_key=True)
    title = Column(String(500), nullable=False)
    description = Column(Text)
    url = Column(String(500))
    summary = Column(Text)
    category = Column(String(100))
    published_at = Column(DateTime)
    created_at = Column(DateTime, default=datetime.utcnow)
    viewer_count = Column(Integer, default=0)

# NOTE: For development, SQLite is fine; consider PostgreSQL for production.
engine = create_engine('sqlite:///blogify.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

@contextmanager
def get_db_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()