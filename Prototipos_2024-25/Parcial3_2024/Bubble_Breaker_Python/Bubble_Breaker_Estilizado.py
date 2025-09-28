# bub2 py
import random
import tkinter as tk
from tkinter import messagebox, ttk

class RompeBurbujas:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🔴 Rompe Burbujas")
        self.root.configure(bg='#1e1e2e')
        self.root.resizable(False, False)

        # Configuración del juego
        self.filas, self.columnas = 10, 10
        self.colores = ["#ff6b6b", "#4ecdc4", "#6aa84f", "#f9ca24", "#6c5ce7", "#fd79a8"]
        self.tamano = 50
        self.puntaje = 0

        # Configurar interfaz
        self.configurar_ui()
        self.nuevo_juego()

    def configurar_ui(self):
        # Frame principal con gradiente simulado
        main_frame = tk.Frame(self.root, bg='#1e1e2e', padx=20, pady=20)
        main_frame.pack()

        # Header con puntaje
        header = tk.Frame(main_frame, bg='#1e1e2e')
        header.pack(fill='x', pady=(0, 15))

        self.label_puntaje = tk.Label(header, text="Puntaje: 0",
                                      font=('Arial', 18, 'bold'),
                                      fg='#f8f8f2', bg='#1e1e2e')
        self.label_puntaje.pack(side='left')

        tk.Button(header, text="🔄 Nuevo Juego", command=self.nuevo_juego,
                  font=('Arial', 12, 'bold'), bg='#6c5ce7', fg='white',
                  relief='flat', padx=20, pady=5,
                  activebackground='#5a4fcf').pack(side='right')

        # Canvas del juego con borde
        canvas_frame = tk.Frame(main_frame, bg='#44475a', relief='solid', bd=2)
        canvas_frame.pack()

        self.canvas = tk.Canvas(canvas_frame, width=self.columnas * self.tamano,
                                height=self.filas * self.tamano, bg='#282a36',
                                highlightthickness=0)
        self.canvas.pack(padx=5, pady=5)
        self.canvas.bind("<Button-1>", self.clic)

    def generar_tablero(self):
        return [[random.choice(self.colores) for _ in range(self.columnas)]
                for _ in range(self.filas)]

    def encontrar_grupo(self, f, c, color=None):
        if not color: color = self.tablero[f][c]
        if not color: return []

        visitados, grupo = set(), [(f, c)]
        for f, c in grupo:
            if (f, c) in visitados: continue
            visitados.add((f, c))
            for df, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nf, nc = f + df, c + dc
                if (0 <= nf < self.filas and 0 <= nc < self.columnas and
                        self.tablero[nf][nc] == color and (nf, nc) not in visitados):
                    grupo.append((nf, nc))
        return grupo if len(grupo) > 1 else []

    def eliminar_grupo(self, grupo):
        for f, c in grupo: self.tablero[f][c] = None
        # Colapsar columnas
        for c in range(self.columnas):
            col = [self.tablero[f][c] for f in range(self.filas) if self.tablero[f][c]]
            for f in range(self.filas):
                self.tablero[f][c] = col[f - self.filas] if f >= self.filas - len(col) else None

    def dibujar(self):
        self.canvas.delete("all")
        for f in range(self.filas):
            for c in range(self.columnas):
                x, y = c * self.tamano, f * self.tamano
                if self.tablero[f][c]:
                    # Burbuja con efecto 3D
                    self.canvas.create_oval(x + 2, y + 2, x + self.tamano - 2, y + self.tamano - 2,
                                            fill=self.tablero[f][c], outline='#6272a4', width=2)
                    # Brillo
                    self.canvas.create_oval(x + 8, y + 8, x + 20, y + 20,
                                            fill='#ffffff', outline='', stipple='gray50')

    def clic(self, e):
        f, c = e.y // self.tamano, e.x // self.tamano
        if (grupo := self.encontrar_grupo(f, c)):
            self.puntaje += len(grupo) * (len(grupo) - 1)
            self.eliminar_grupo(grupo)
            self.dibujar()
            self.label_puntaje.config(text=f"Puntaje: {self.puntaje}")

            if not any(self.tablero[f][c] and self.encontrar_grupo(f, c)
                       for f in range(self.filas) for c in range(self.columnas)):
                messagebox.showinfo("🎉 ¡Fin del juego!",
                                    f"Puntaje final: {self.puntaje}\n¡Bien jugado!")
                self.nuevo_juego()

    def nuevo_juego(self):
        self.tablero = self.generar_tablero()
        self.puntaje = 0
        self.label_puntaje.config(text="Puntaje: 0")
        self.dibujar()

    def iniciar(self):
        self.root.mainloop()


if __name__ == "__main__":
    RompeBurbujas().iniciar()