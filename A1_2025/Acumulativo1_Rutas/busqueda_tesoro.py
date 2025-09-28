import tkinter as tk
import tkinter.font as tkFont

# Nota Acumulativa 01

def main():
    root= tk.Tk()
    root.geometry("440x220")
    root.title("Acumulativo - Busqueda del Tesoro")
    root.configure(bg='#00809D')

    fuente = tkFont.Font(family="Calibri", size=14, weight="bold")

    label = tk.Label(root, text="MAPA & BUSQUEDA DEL TESORO\n"
                                "Se ha creado con exito la salida ruta_tesoro.txt", font=fuente, bg='#00809D', fg='#ffffff')
    label.pack(pady=20)

    caja = tkFont.Font(family="Arial", size=11, weight="bold")
    caja = tk.Text(root, font=caja, height=5, width=30, bg='#F3A26D', fg='#ffffff')
    caja.pack()

    #Movimientos del pirata
    def encontrar_ruta(cuadricula, pirata_max, tamano):
        direcciones = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}

        def buscar_ruta(posicion_actual, pasos, ruta_actual, visitados, pirata):
            x, y = posicion_actual
            # Hallar T Tesoro
            if cuadricula[x][y] == 'T':
                return pasos, ruta_actual

            visitados.add(posicion_actual)

            for direccion, (dx, dy) in direcciones.items():
                nueva_x, nueva_y = x + dx, y + dy
                nueva_posicion = (nueva_x, nueva_y)

                if 0 <= nueva_x < tamano and 0 <= nueva_y < tamano:
                    if cuadricula[nueva_x][nueva_y] != '#' and nueva_posicion not in visitados:
                        if cuadricula[nueva_x][nueva_y] == 'X':
                            if pirata < pirata_max:
                                resultado, camino = buscar_ruta(nueva_posicion, pasos + 1, ruta_actual + [direccion],
                                                                visitados, pirata + 1)
                                if resultado != -1:
                                    return resultado, camino
                        else:
                            resultado, camino = buscar_ruta(nueva_posicion, pasos + 1, ruta_actual + [direccion],
                                                            visitados, pirata)
                            if resultado != -1:
                                return resultado, camino

            visitados.remove(posicion_actual)
            return -1, []

        entrada = None
        for i in range(tamano):
            for j in range(tamano):
                if cuadricula[i][j] == 'E':
                    entrada = (i, j)
                    break
            if entrada:
                break

        if not entrada:
            print("Tesoro no encontrado")
            return -1, []

        return buscar_ruta(entrada, 0, [], set(), 0)

    def main():
        cuadricula = []
        resultado = None

        try:
            with open('mapa_pirata.txt', 'r', encoding='utf-8') as archivo:
                pirata_max = int(archivo.readline().strip())
                tamano = int(archivo.readline().strip())
                for _ in range(tamano):
                    fila = archivo.readline().strip()
                    cuadricula.append(list(fila))

            resultado = encontrar_ruta(cuadricula, pirata_max, tamano)
        except FileNotFoundError:
            print("No se encontró el archivo de entrada")

        if resultado is not None:
            with open('ruta_tesoro.txt', 'w', encoding='utf-8') as salida:
                salida.write(str(resultado[0]) + '\n')
                if resultado[0] != -1:
                    salida.write(''.join(resultado[1]))
                print("Se creó el archivo de salida con la ruta hacia el Tesoro")

    if __name__ == "__main__":
        main()

    root.mainloop()


if __name__ == "__main__":
    main()
