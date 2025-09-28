# raices digital
import tkinter as tk
from tkinter import filedialog, messagebox

def leer_lineas(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        lineas = archivo.readlines()
    return [linea.strip() for linea in lineas]

def raiz_digital(numero):
    while numero >= 10:
        suma = 0
        while numero > 0:
            suma += numero % 10
            numero = numero // 10
        numero = suma
    return numero

def calcular_y_mostrar():
    nombre_archivo = filedialog.askopenfilename(title="Seleccionar archivo")
    if not nombre_archivo:
        return

    try:
        lineas = leer_lineas(nombre_archivo)
    except Exception as err:
        messagebox.showerror("Error", f"Error al leer el archivo: {err}")
        return

    print("Informacion del documento:")
    numeros = []
    for linea in lineas:
        try:
            numero = int(linea)
            print(numero)
            if numero == 0:
                break
            numeros.append(numero)
        except ValueError as err:
            print(f"Error al convertir la informacion en un número: {err}")

    print("\nRaiz digital:")
    resultados = []
    for numero in numeros:
        raiz = raiz_digital(numero)
        print(raiz)
        resultados.append(f"Raiz digital de {numero} es {raiz}")

    # Mostrar resultados en la interfaz grafica
    resultado_label.config(text="\n".join(resultados))

ventana = tk.Tk()
ventana.title("Raices Digitales")
ventana.geometry("500x400")
ventana.configure(bg='#98A1BC')

titulo_label = tk.Label(ventana, text="CALCULADORA DE RAICES DIGITALES", font=("Calibri", 15, "bold"), bg='#98A1BC', fg='#333333')
titulo_label.pack(pady=15)

calcular_boton = tk.Button(ventana, text="Seleccionar Archivo", command=calcular_y_mostrar, bg='#EAA64D', fg='#333333',font=("Calibri", 10))
calcular_boton.pack(pady=20)

resultado_label = tk.Label(ventana, text="", justify=tk.LEFT, bg='#DED3C4', fg='#333333', width=50, height=10, font=("Calibri", 12))
resultado_label.pack(pady=10)

ventana.mainloop()
