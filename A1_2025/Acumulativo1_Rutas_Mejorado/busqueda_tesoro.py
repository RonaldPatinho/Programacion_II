from PIL import Image, ImageDraw, ImageFont

def encontrar_ruta(cuadricula, pirata_max, tamano):
    direcciones = {'N': (-1, 0), 'S': (1, 0), 'E': (0, 1), 'O': (0, -1)}

    def buscar_ruta(posicion_actual, pasos, ruta_actual, visitados, pirata):
        x, y = posicion_actual
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
                            resultado, camino = buscar_ruta(nueva_posicion, pasos + 1, ruta_actual + [direccion], visitados, pirata + 1)
                            if resultado != -1:
                                return resultado, camino
                    else:
                        resultado, camino = buscar_ruta(nueva_posicion, pasos + 1, ruta_actual + [direccion], visitados, pirata)
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
        print("Entrada no encontrada")
        return -1, []

    return buscar_ruta(entrada, 0, [], set(), 0)

def generar_imagen(cuadricula, ruta, tamano):
    colores = {
        'E': 'green',
        'T': 'gold',
        '#': 'black',
        '.': 'white',
        'X': 'red',
    }

    celda_tamano = 50
    imagen_tamano = tamano * celda_tamano

    imagen = Image.new('RGB', (imagen_tamano, imagen_tamano), 'white')
    draw = ImageDraw.Draw(imagen)

    # Dibuja la cuadricula
    for i in range(tamano):
        for j in range(tamano):
            color = colores.get(cuadricula[i][j], 'white')
            draw.rectangle([j * celda_tamano, i * celda_tamano, (j + 1) * celda_tamano, (i + 1) * celda_tamano], fill=color)

    # Ruta
    x, y = next((i, j) for i in range(tamano) for j in range(tamano) if cuadricula[i][j] == 'E')
    for direccion in ruta:
        if direccion == 'N':
            x -= 1
        elif direccion == 'S':
            x += 1
        elif direccion == 'E':
            y += 1
        elif direccion == 'O':
            y -= 1
        draw.ellipse([y * celda_tamano + 10, x * celda_tamano + 10, (y + 1) * celda_tamano - 10, (x + 1) * celda_tamano - 10], fill='blue')

    imagen.save('mapa_solucion.png')

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
        return

    if resultado is not None:
        pasos, ruta = resultado
        with open('ruta_tesoro.txt', 'w', encoding='utf-8') as salida:
            salida.write(str(pasos) + '\n')
            if pasos != -1:
                salida.write(''.join(ruta))
        print("Se creó el archivo de salida con la ruta hacia el Tesoro")

        if pasos != -1:
            generar_imagen(cuadricula, ruta, tamano)
            print("Se generó la imagen del mapa con la ruta hacia el Tesoro")

if __name__ == "__main__":
    main()
