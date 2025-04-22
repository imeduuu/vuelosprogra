class Nodo:
    def __init__(self, vuelo):
        self.vuelo = vuelo
        self.anterior = None
        self.siguiente = None

class ListaDoblementeEnlazada:
    def __init__(self):
        self.primero = None
        self.ultimo = None
        self.size = 0

    def insertar_al_frente(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.primero:
            self.primero = self.ultimo = nuevo
        else:
            nuevo.siguiente = self.primero
            self.primero.anterior = nuevo
            self.primero = nuevo
        self.size += 1

    def insertar_al_final(self, vuelo):
        nuevo = Nodo(vuelo)
        if not self.ultimo:
            self.primero = self.ultimo = nuevo
        else:
            self.ultimo.siguiente = nuevo
            nuevo.anterior = self.ultimo
            self.ultimo = nuevo
        self.size += 1

    def obtener_primero(self):
        return self.primero.vuelo if self.primero else None

    def obtener_ultimo(self):
        return self.ultimo.vuelo if self.ultimo else None

    def longitud(self):
        return self.size

    def insertar_en_posicion(self, vuelo, posicion):
        if posicion <= 0:
            self.insertar_al_frente(vuelo)
        elif posicion >= self.size:
            self.insertar_al_final(vuelo)
        else:
            nuevo = Nodo(vuelo)
            actual = self.primero
            for _ in range(posicion):
                actual = actual.siguiente
            anterior = actual.anterior
            anterior.siguiente = nuevo
            nuevo.anterior = anterior
            nuevo.siguiente = actual
            actual.anterior = nuevo
            self.size += 1

    def extraer_de_posicion(self, posicion):
        if posicion < 0 or posicion >= self.size:
            return None
        actual = self.primero
        for _ in range(posicion):
            actual = actual.siguiente
        if actual.anterior:
            actual.anterior.siguiente = actual.siguiente
        else:
            self.primero = actual.siguiente
        if actual.siguiente:
            actual.siguiente.anterior = actual.anterior
        else:
            self.ultimo = actual.anterior
        self.size -= 1
        return actual.vuelo

    def buscar_posicion_por_id(self, vuelo_id):
        actual = self.primero
        posicion = 0

        while actual:
            if hasattr(actual.vuelo, 'id') and actual.vuelo.id == vuelo_id:
                return posicion
            actual = actual.siguiente
            posicion += 1

        return None

lista = ListaDoblementeEnlazada()