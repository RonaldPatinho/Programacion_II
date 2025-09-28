# reloj
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

def leer_archivo(nombre_archivo):
    try:
        with open(nombre_archivo, 'r', encoding="utf-8") as archivo:
            horas_leidas = [linea.split() for linea in archivo.readlines()]
            tiempos = []
            for hora in horas_leidas:
                if len(hora) == 4:
                    hora_inicio, minuto_inicio, hora_fin, minuto_fin = map(int, hora)
                    tiempos.append((hora_inicio, minuto_inicio, hora_fin, minuto_fin))
                else:
                    messagebox.showwarning("Advertencia", "El archivo de entrada no cumple con los parámetros establecidos.")
                    return []
    except FileNotFoundError:
        messagebox.showerror("Error", "El archivo no fue encontrado!")
        return []

    return tiempos

def contar_cruces_horas(hora_inicio, minuto_inicio, hora_fin, minuto_fin):
    tiempo_inicio_total = hora_inicio * 60 + minuto_inicio
    tiempo_fin_total = hora_fin * 60 + minuto_fin

    if tiempo_fin_total <= tiempo_inicio_total:
        tiempo_fin_total += 12 * 60

    intervalos_tiempo = 0
    angulo_minuto = 360 / 60
    angulo_hora = 360 / 12 / 60

    angulo_hora_actual = (hora_inicio % 12) * 30 + minuto_inicio * 0.5
    angulo_minuto_actual = minuto_inicio * angulo_minuto

    angulo_hora_anterior = angulo_hora_actual
    angulo_minuto_anterior = angulo_minuto_actual

    for _ in range(tiempo_inicio_total, tiempo_fin_total):
        angulo_hora_actual += angulo_hora
        angulo_minuto_actual += angulo_minuto

        if angulo_hora_actual >= 360:
            angulo_hora_actual -= 360
        if angulo_minuto_actual >= 360:
            angulo_minuto_actual -= 360

        if (angulo_minuto_anterior <= angulo_hora_anterior < angulo_minuto_actual) or (
                angulo_minuto_anterior < angulo_hora_actual <= angulo_minuto_actual):
            intervalos_tiempo += 1

        angulo_hora_anterior = angulo_hora_actual
        angulo_minuto_anterior = angulo_minuto_actual

    return intervalos_tiempo

class RelojApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cruces de Manecillas del Reloj")

        # Botón para cargar el archivo
        tk.Button(root, text="Cargar Archivo", command=self.cargar_archivo, bg='#4CAF50', fg='white').pack(pady=10)

        # Configuración del Treeview
        self.tree = ttk.Treeview(root, columns=("Tiempo Inicial", "Tiempo Final", "Pasadas"), show="headings")
        self.tree.heading("Tiempo Inicial", text="Tiempo Inicial")
        self.tree.heading("Tiempo Final", text="Tiempo Final")
        self.tree.heading("Pasadas", text="Pasadas")

        self.tree.column("Tiempo Inicial", anchor="center", width=100)
        self.tree.column("Tiempo Final", anchor="center", width=100)
        self.tree.column("Pasadas", anchor="center", width=100)

        self.tree.pack(pady=10)

    def cargar_archivo(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.in")])
        if file_path:
            # Limpiar el Treeview antes de cargar nuevos datos
            for item in self.tree.get_children():
                self.tree.delete(item)
            intervalos_tiempo = leer_archivo(file_path)
            self.mostrar_resultados(intervalos_tiempo)

    def mostrar_resultados(self, intervalos_tiempo):
        for intervalo in intervalos_tiempo:
            hora_inicio, minuto_inicio, hora_fin, minuto_fin = intervalo
            cruces = contar_cruces_horas(hora_inicio, minuto_inicio, hora_fin, minuto_fin)
            self.tree.insert("", "end", values=(
                f"{hora_inicio:02d}:{minuto_inicio:02d}",
                f"{hora_fin:02d}:{minuto_fin:02d}",
                cruces
            ))

def main():
    root = tk.Tk()
    app = RelojApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
