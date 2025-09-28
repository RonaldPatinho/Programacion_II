import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont

# Ejercicio2 Diccionario de prefijos de palabras

def contar_palabras_con_prefijos(diccionario, prefijos):
    return {prefijo: sum(1 for palabra in diccionario if palabra.startswith(prefijo)) for prefijo in prefijos}

def procesar_y_mostrar():
    try:
        entrada_palabras = palabras_entrada.get("1.0", tk.END).strip().split()
        entrada_prefijos = prefijos_entrada.get("1.0", tk.END).strip().split()

        conteos = contar_palabras_con_prefijos(entrada_palabras, entrada_prefijos)


        texto_resultado = "\n".join(f"Prefijo '{prefijo}': {conteo}" for prefijo, conteo in conteos.items())
        messagebox.showinfo("Resultados", texto_resultado)

    except Exception as e:
        messagebox.showerror("Error", f"Ocurrió un error: {e}")

def interfaz_principal():
    root = tk.Tk()
    root.title("Ejercicio 2 - Diccionario de prefijos de palabras")
    root.geometry("500x300")
    root.configure(bg='#00809D')

    fuente_texto = tkFont.Font(family="Calibri", size=12, weight="bold")
    fuente_boton = tkFont.Font(family="Calibri", size=10, weight="bold")

    etiqueta_palabras = tk.Label(root, text="1. Ingresa PALABRAS separadas por espacios:", font=fuente_texto, bg='#00738E', fg='#ffffff')
    etiqueta_palabras.pack(pady=5)

    global palabras_entrada
    palabras_entrada = tk.Text(root, height=5, width=50, font=tkFont.Font(family="Arial", size=12), bg='#454545', fg='#ffffff')
    palabras_entrada.pack(pady=5)

    etiqueta_prefijos = tk.Label(root, text="2. Ingresa PREFIJOS separados por espacios:", font=fuente_texto, bg='#00738E', fg='#ffffff')
    etiqueta_prefijos.pack(pady=5)

    global prefijos_entrada
    prefijos_entrada = tk.Text(root, height=2, width=50, font=tkFont.Font(family="Arial", size=12), bg='#454545', fg='#ffffff')
    prefijos_entrada.pack(pady=5)

    boton_procesar = tk.Button(root, text="CONTAR",font=fuente_boton, command=procesar_y_mostrar, bg='#F3A26D', fg='#D33E03')
    boton_procesar.pack(pady=10)


    # Metodo para leer entrada y expulsar salida
    def conteo_generar(dic, prefixes):
        return {prefix: sum(1 for palabra2 in dic if palabra2.startswith(prefix)) for prefix in prefixes}

    def archivo():
        try:
            with open('palabras.txt', 'r', encoding='utf-8') as file:
                lineas = file.readlines()
                numpalabras = int(lineas[0].strip())
                dic = [lineas[i].strip().lower() for i in range(1, numpalabras + 1)]
                numprefijos = int(lineas[numpalabras + 1].strip())
                prefixes = [lineas[i].strip() for i in range(numpalabras + 2, numpalabras + 2 + numprefijos)]

            counts = conteo_generar(dic, prefixes)

            with open('salidapalabras.txt', 'w', encoding='utf-8') as output:
                output.write(' '.join(map(str, counts.values())))
                print("El archivo de salida fue creado exitosamente")

        except FileNotFoundError:
            print("El archivo no fue encontrado")

    if __name__ == "__main__":
        archivo()

    root.mainloop()

if __name__ == "__main__":
    interfaz_principal()