import atexit
from sqlalchemy import Column, String, Integer, DateTime, create_engine, ForeignKey, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

PG_DSN = 'postgresql://wooft:Shambala@127.0.0.1:5432/flask_db'

engine = create_engine(PG_DSN)

Base = declarative_base()
Session = sessionmaker(bind=engine)

atexit.register(engine.dispose)

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)


class Announcement(Base):
    __tablename__ = 'announcement'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False, index=True)
    description = Column(String)
    creation_time = Column(DateTime, server_default=func.now())
    owner = Column(Integer, ForeignKey(User.id))