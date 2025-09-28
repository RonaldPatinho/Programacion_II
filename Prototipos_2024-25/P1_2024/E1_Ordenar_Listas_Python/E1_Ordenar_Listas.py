import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext

def proceso_de_ordenamiento(lista):
    palabras = []
    numeros = []
    for elemento in lista:
        if elemento.replace('-', '').isdigit():
            numeros.append(elemento)
        else:
            palabras.append(elemento)
    numeros_ordenados = sorted(numeros, key=asignar_signo)
    palabras_ordenadas = sorted(palabras, key=str.lower)
    lista_ordenada = []
    indice_palabra = 0
    indice_numero = 0
    for elemento in lista:
        if elemento.replace('-', '').isdigit():
            lista_ordenada.append(numeros_ordenados[indice_numero])
            indice_numero += 1
        else:
            lista_ordenada.append(palabras_ordenadas[indice_palabra])
            indice_palabra += 1
    return lista_ordenada

def asignar_signo(num):
    if '-' not in num:
        return int(num)
    else:
        numero_sin_signo = int(num[1:])
        numero_con_signo = 0 - numero_sin_signo
        return numero_con_signo

def procesar_archivo(archivo_entrada, entrada_text, salida_text):
    try:
        with open(archivo_entrada, 'r', encoding='utf-8') as archivo:
            lineas = archivo.readlines()

        entrada_text.config(state=tk.NORMAL)
        entrada_text.delete(1.0, tk.END)
        entrada_text.insert(tk.INSERT, "".join(lineas))
        entrada_text.config(state=tk.DISABLED)

        salida = []
        for linea in lineas:
            if linea.strip() == '.':
                break
            elementos = linea.strip().rstrip('.').split(', ')
            lista_ordenada = proceso_de_ordenamiento(elementos)
            ver_lista_ordenada = ', '.join(lista_ordenada)
            salida.append(ver_lista_ordenada + '.')

        salida_text.config(state=tk.NORMAL)
        salida_text.delete(1.0, tk.END)
        salida_text.insert(tk.INSERT, "\n".join(salida))
        salida_text.config(state=tk.DISABLED)

        with open('Salida.out', 'w', encoding='utf-8') as archivo_salida:
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
    ventana.title("Ordenador de Listas")
    ventana.geometry("600x500")
    ventana.configure(bg='#98A1BC')

    titulo_label = tk.Label(ventana, text="ORDENADOR DE LISTAS", font=("Calibri", 15, "bold"), bg='#98A1BC', fg='#333333')
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
