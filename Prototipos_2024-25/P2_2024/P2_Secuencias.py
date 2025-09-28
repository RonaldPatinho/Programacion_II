import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def procesar_secuencia(fredy):
    longitud_secuencia = 1
    maria = 0
    longitud_maxima_secuencia = 0
    i = 0
    while i < len(fredy) - 1:
        if maria % 2 == 0 and fredy[i] > fredy[i + 1]:
            longitud_secuencia += 1
            maria += 1
        elif maria % 2 == 1:
            if fredy[i] < fredy[i + 1]:
                longitud_secuencia += 1
                maria += 1
            else:
                if longitud_secuencia > longitud_maxima_secuencia:
                    longitud_maxima_secuencia = longitud_secuencia
                i = i - 1
                maria = 0
                longitud_secuencia = 1
        else:
            if longitud_secuencia > longitud_maxima_secuencia:
                longitud_maxima_secuencia = longitud_secuencia
            maria = 0
            longitud_secuencia = 1
        i = i + 1
    longitud_secuencia = max(longitud_secuencia, longitud_maxima_secuencia)
    return longitud_secuencia

def procesar_archivo(archivo_entrada, entrada_text, salida_text):
    try:
        with open(archivo_entrada, 'r', encoding="utf-8") as archivo:
            lineas = archivo.readlines()

        entrada_text.config(state=tk.NORMAL)
        entrada_text.delete(1.0, tk.END)
        entrada_text.insert(tk.INSERT, "".join(lineas))
        entrada_text.config(state=tk.DISABLED)

        salida = []
        num_casos = int(lineas[0].strip())
        if num_casos < 1 or num_casos > 50:
            messagebox.showerror("Error", "El número de casos de prueba no se encuentra dentro del rango establecido")
            return

        for i in range(1, num_casos + 1):
            linea = lineas[i].strip().split()
            n = int(linea[0])
            if n < 1 or n > 30000:
                messagebox.showerror("Error", "El número de elementos no se encuentra dentro del rango establecido")
                return
            if n != len(linea) - 1:
                messagebox.showerror("Error", f"El número de elementos no coincide con el valor de n en la línea: {linea}")
                return
            fredy = list(map(int, linea[1:]))
            resultado = procesar_secuencia(fredy)
            salida.append(f"Longitud de la secuencia más larga: {resultado}")

        salida_text.config(state=tk.NORMAL)
        salida_text.delete(1.0, tk.END)
        salida_text.insert(tk.INSERT, "\n".join(salida))
        salida_text.config(state=tk.DISABLED)

        with open('salida15.out', 'w', encoding="utf-8") as archivo_salida:
            archivo_salida.write("\n".join(salida))

        messagebox.showinfo("Éxito", "El archivo de salida ha sido creado exitosamente!")

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def seleccionar_archivo(entrada_text, salida_text):
    archivo_entrada = filedialog.askopenfilename(title="Seleccionar archivo de entrada", filetypes=[("Text files", "*.in")])
    if archivo_entrada:
        procesar_archivo(archivo_entrada, entrada_text, salida_text)

def main():
    ventana = tk.Tk()
    ventana.title("Procesador de Secuencias")
    ventana.geometry("600x500")
    ventana.configure(bg='#98A1BC')

    titulo_label = tk.Label(ventana, text="PROCESADOR DE SECUENCIAS", font=("Calibri", 15, "bold"), bg='#98A1BC', fg='#333333')
    titulo_label.pack(pady=10)

    boton_seleccionar = tk.Button(ventana, text="Seleccionar Archivo", command=lambda: seleccionar_archivo(entrada_text, salida_text), bg='#EAA64D', fg='#333333', font=("Calibri", 10))
    boton_seleccionar.pack(pady=10)

    entrada_label = tk.Label(ventana, text="Entrada:", bg='#98A1BC', fg='#333333', font=("Calibri", 12, "bold"))
    entrada_label.pack(pady=(10, 0))

    entrada_text = scrolledtext.ScrolledText(ventana, width=60, height=10, font=("Calibri", 10), state=tk.DISABLED)
    entrada_text.pack(pady=5)

    salida_label = tk.Label(ventana, text="Salida:", bg='#98A1BC', fg='#333333', font=("Calibri", 12, "bold"))
    salida_label.pack(pady=(10, 0))

    salida_text = scrolledtext.ScrolledText(ventana, width=60, height=10, font=("Calibri", 10), state=tk.DISABLED)
    salida_text.pack(pady=5)

    ventana.mainloop()

if __name__ == "__main__":
    main()
