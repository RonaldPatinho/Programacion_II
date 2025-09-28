import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

class PirateMapApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Busqueda del Tesoro")
        self.root.geometry("800x600")
        self.root.configure(bg='#FAD59A')

        style = ttk.Style()
        style.configure("Title.TLabel", foreground="#E9A319", background="#FAD59A", font=('Calibri', 17, 'bold'))

        title_label = ttk.Label(root, text="MAPA DEL TESORO", style="Title.TLabel")
        title_label.place(relx=0.5, rely=0.03, anchor=tk.CENTER)

        self.map_frame = ttk.Frame(root, style="White.TFrame")
        self.map_frame.pack(pady=40)

        style.configure("White.TFrame", background="white")

        self.load_button = ttk.Button(root, text="Mostrar Solución", command=self.show_solution)
        self.load_button.pack(pady=5)

        self.image_frame = ttk.Frame(root)
        self.image_frame.pack(pady=5)

        self.load_pirate_map()

    def load_pirate_map(self):
        try:
            with open('mapa_pirata.txt', 'r') as file:
                lines = file.readlines()
                # Leer K y N
                k = lines[0].strip()
                n = lines[1].strip()

                # Mostrar K y N
                ttk.Label(self.map_frame, text=k, font=('Calibri', 12), background='white').grid(row=0, column=0, pady=2)
                ttk.Label(self.map_frame, text=n, font=('Calibri', 12), background='white').grid(row=1, column=0, pady=2)

                # Mostrar el mapa
                for i, line in enumerate(lines[2:], start=2):
                    for j, char in enumerate(line.strip()):
                        label = ttk.Label(self.map_frame, text=char, font=('Courier', 12), width=2, relief="solid", background='white')
                        label.grid(row=i, column=j, padx=0, pady=0)

        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo mapa_pirata.txt no fue encontrado.")

    def show_solution(self):
        try:

            image = Image.open("mapa_solucion.png")
            photo = ImageTk.PhotoImage(image)

            if hasattr(self, 'image_label'):
                self.image_label.configure(image=photo)
                self.image_label.image = photo
            else:
                self.image_label = ttk.Label(self.image_frame, image=photo, background='#FAD59A')
                self.image_label.image = photo
                self.image_label.pack()
        except FileNotFoundError:
            messagebox.showerror("Error", "El archivo mapa_solucion.png no fue encontrado.")

def main():
    root = tk.Tk()
    app = PirateMapApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
