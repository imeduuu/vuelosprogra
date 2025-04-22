from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, inicializar_db
import crud
from models import Vuelo
from pydantic import BaseModel

app = FastAPI()

inicializar_db()

# Dependencia para obtener la DB
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class VueloIn(BaseModel):
    codigo: str
    destino: str
    prioridad: str

@app.post("/vuelos/", response_model=dict)
def crear_vuelo(vuelo: VueloIn, db: Session = Depends(get_db)):
    nuevo = crud.crear_vuelo(db, vuelo.dict())
    return {"mensaje": "Vuelo creado", "id": nuevo.id}

@app.get("/vuelos/", response_model=list)
def listar_vuelos(db: Session = Depends(get_db)):
    return crud.obtener_vuelos(db)

@app.get("/vuelos/{vuelo_id}")
def obtener_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    vuelo = crud.obtener_vuelo(db, vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return vuelo

@app.put("/vuelos/{vuelo_id}")
def actualizar_vuelo(vuelo_id: int, vuelo: VueloIn, db: Session = Depends(get_db)):
    actualizado = crud.actualizar_vuelo(db, vuelo_id, vuelo.dict())
    if not actualizado:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return {"mensaje": "Vuelo actualizado"}

@app.delete("/vuelos/{vuelo_id}")
def eliminar_vuelo(vuelo_id: int, db: Session = Depends(get_db)):
    eliminado = crud.eliminar_vuelo(db, vuelo_id)
    if not eliminado:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")
    return {"mensaje": "Vuelo eliminado"}
