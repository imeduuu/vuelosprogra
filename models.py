from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Vuelo(Base):
    __tablename__ = "vuelos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, nullable=False)
    destino = Column(String, nullable=False)
    prioridad = Column(String, nullable=False)  # "emergencia" o "regular"
