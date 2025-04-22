from models import Vuelo
from sqlalchemy.orm import Session

def crear_vuelo(db: Session, datos):
    vuelo = Vuelo(**datos)
    db.add(vuelo)
    db.commit()
    db.refresh(vuelo)
    return vuelo

def obtener_vuelos(db: Session):
    return db.query(Vuelo).all()

def obtener_vuelo(db: Session, vuelo_id: int):
    return db.query(Vuelo).filter(Vuelo.id == vuelo_id).first()

def actualizar_vuelo(db: Session, vuelo_id: int, datos):
    vuelo = obtener_vuelo(db, vuelo_id)
    if vuelo:
        for key, value in datos.items():
            setattr(vuelo, key, value)
        db.commit()
        db.refresh(vuelo)
    return vuelo

def eliminar_vuelo(db: Session, vuelo_id: int):
    vuelo = obtener_vuelo(db, vuelo_id)
    if vuelo:
        db.delete(vuelo)
        db.commit()
    return vuelo
