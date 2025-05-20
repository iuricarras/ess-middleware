from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import sessionmaker, declarative_base
from dataclasses import dataclass

db = create_engine("sqlite:///sqlite.db")
Session = sessionmaker(bind=db)
session = Session()

Base = declarative_base()

@dataclass
class VM(Base):
    __tablename__ = "vms"

    id = Column(Integer, primary_key=True)
    name:str = Column(String(50), unique=True)


    def __init__(self, name):
        self.name = name


Base.metadata.create_all(bind=db)

import package.ws
