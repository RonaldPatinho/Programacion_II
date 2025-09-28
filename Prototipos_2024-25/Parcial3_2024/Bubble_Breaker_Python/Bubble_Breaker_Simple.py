# bub
import random
import tkinter as tk
from tkinter import messagebox

class JuegoRompeBurbujas:
    def __init__(self):
        self.filas = 10
        self.columnas = 10
        self.colores = ["red", "green", "blue", "yellow", "purple", "pink"]
        self.tablero = self.generar_tablero()

    def generar_tablero(self):
        return [[random.choice(self.colores) for _ in range(self.columnas)] for _ in range(self.filas)]

    def encontrar_grupo(self, fila, columna):
        color = self.tablero[fila][columna]
        por_revisar = [(fila, columna)]
        grupo = []
        while por_revisar:
            f, c = por_revisar.pop()
            if (f, c) not in grupo:
                grupo.append((f, c))
                for df, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    nf, nc = f + df, c + dc
                    if 0 <= nf < self.filas and 0 <= nc < self.columnas and self.tablero[nf][nc] == color:
                        por_revisar.append((nf, nc))
        return grupo if len(grupo) > 1 else []

    def eliminar_grupo(self, grupo):
        for f, c in grupo:
            self.tablero[f][c] = None
        self.colapsar_tablero()

    def colapsar_tablero(self):
        for c in range(self.columnas):
            columna = [self.tablero[f][c] for f in range(self.filas) if self.tablero[f][c] is not None]
            for f in range(self.filas - len(columna)):
                self.tablero[f][c] = None
            for f in range(self.filas - len(columna), self.filas):
                self.tablero[f][c] = columna[f - (self.filas - len(columna))]

    def tiene_movimientos(self):
        return any(self.tablero[f][c] and self.encontrar_grupo(f, c) for f in range(self.filas) for c in range(self.columnas))

    def calcular_puntaje(self, tamano_grupo):
        return tamano_grupo * (tamano_grupo - 1)

class AplicacionRompeBurbujas:
    def __init__(self, root):
        self.root = root
        self.root.title("Rompe Burbujas")
        self.juego = JuegoRompeBurbujas()
        self.puntaje = 0
        self.canvas = tk.Canvas(self.root, width=600, height=600)
        self.canvas.pack()
        self.etiqueta_puntaje = tk.Label(self.root, text="Puntaje: 0")
        self.etiqueta_puntaje.pack()
        self.boton_nuevo_juego = tk.Button(self.root, text="Nuevo Juego", command=self.nuevo_juego)
        self.boton_nuevo_juego.pack()
        self.canvas.bind("<Button-1>", self.manejar_clic)
        self.dibujar_tablero()

    def dibujar_tablero(self):
        self.canvas.delete("all")
        tamano = 60
        for f in range(self.juego.filas):
            for c in range(self.juego.columnas):
                if self.juego.tablero[f][c]:
                    self.canvas.create_oval(c * tamano, f * tamano, c * tamano + tamano, f * tamano + tamano,
                                           fill=self.juego.tablero[f][c])

    def manejar_clic(self, event):
        tamano = 60
        c, f = event.x // tamano, event.y // tamano
        if 0 <= f < self.juego.filas and 0 <= c < self.juego.columnas:
            if (grupo := self.juego.encontrar_grupo(f, c)):
                self.puntaje += self.juego.calcular_puntaje(len(grupo))
                self.juego.eliminar_grupo(grupo)
                self.dibujar_tablero()
                self.actualizar_puntaje()
                if not self.juego.tiene_movimientos():
                    messagebox.showinfo("¡Fin del juego!", f"Puntaje final: {self.puntaje}")
                    self.nuevo_juego()

    def actualizar_puntaje(self):
        self.etiqueta_puntaje.config(text=f"Puntaje: {self.puntaje}")

    def nuevo_juego(self):
        self.juego = JuegoRompeBurbujas()
        self.puntaje = 0
        self.actualizar_puntaje()
        self.dibujar_tablero()

def main():
    root = tk.Tk()
    app = AplicacionRompeBurbujas(root)
    root.mainloop()

if __name__ == "__main__":
    main()
