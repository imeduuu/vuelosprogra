from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, inicializar_db
import crud
from models import Vuelo
from pydantic import BaseModel

from lista import lista
from undo import registrar_operacion, deshacer, rehacer

app = FastAPI()

inicializar_db()

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

    lista.insertar_al_final(nuevo)

    posicion = lista.longitud() - 1
    registrar_operacion("eliminar", posicion, nuevo)

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
    vuelo = crud.obtener_vuelo(db, vuelo_id)
    if not vuelo:
        raise HTTPException(status_code=404, detail="Vuelo no encontrado")

    posicion = lista.buscar_posicion_por_id(vuelo_id)
    if posicion is None:
        raise HTTPException(status_code=404, detail="Vuelo no está en la lista")

    lista.extraer_de_posicion(posicion)

    registrar_operacion("insertar", posicion, vuelo)

    crud.eliminar_vuelo(db, vuelo_id)

    return {"mensaje": "Vuelo eliminado"}

@app.post("/vuelos/undo")
def endpoint_deshacer():
    resultado = deshacer(lista)
    return {"mensaje": resultado}

@app.post("/vuelos/redo")
def endpoint_rehacer():
    resultado = rehacer(lista)
    return {"mensaje": resultado}
