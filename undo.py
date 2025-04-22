undo_stack = []
redo_stack = []

def registrar_operacion(accion, posicion, vuelo):
    """
    Guarda la operación en la pila de undo. 
    Al registrar una nueva operación, se borra el historial de redo.
    """
    undo_stack.append((accion, posicion, vuelo))
    redo_stack.clear()


def deshacer(lista):
    """
    Deshace la última operación registrada y la guarda en la pila de redo.
    """
    if not undo_stack:
        return "No hay acciones para deshacer"
    
    accion, posicion, vuelo = undo_stack.pop()

    if accion == "insertar":
        vuelo_extraido = lista.extraer_de_posicion(posicion)
        redo_stack.append(("insertar", posicion, vuelo_extraido))
        return f"Deshecho: se eliminó vuelo en posición {posicion}"
    
    elif accion == "eliminar":
        lista.insertar_en_posicion(vuelo, posicion)
        redo_stack.append(("eliminar", posicion, vuelo))
        return f"Deshecho: se insertó vuelo en posición {posicion}"


def rehacer(lista):
    """
    Rehace la última operación deshecha y la guarda nuevamente en la pila de undo.
    """
    if not redo_stack:
        return "No hay acciones para rehacer"
    
    accion, posicion, vuelo = redo_stack.pop()

    if accion == "insertar":
        lista.insertar_en_posicion(vuelo, posicion)
        undo_stack.append(("eliminar", posicion, vuelo))
        return f"Rehecho: se insertó vuelo en posición {posicion}"

    elif accion == "eliminar":
        vuelo_extraido = lista.extraer_de_posicion(posicion)
        undo_stack.append(("insertar", posicion, vuelo_extraido))
        return f"Rehecho: se eliminó vuelo en posición {posicion}"
