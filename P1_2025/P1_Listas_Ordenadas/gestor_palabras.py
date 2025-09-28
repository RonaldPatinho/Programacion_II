import unicodedata
import re

# P1 Listas de Ordenamiento

class GestorPalabras:
    """
    Clase que inicializa las rutas de los archivos de texto de las palabras y excepciones
    """
    def __init__(self, ruta_texto, ruta_prohibidas):

        self.ruta_texto = ruta_texto
        self.ruta_prohibidas = ruta_prohibidas
        self.frecuencia_palabra = {}
        self.lista_excepciones = set()

    def cargar_excepciones(self):
        """
        Funcion que carga las palabras prohibidas desde el archivo y las almacena en un conjunto
        """
        try:
            with open(self.ruta_prohibidas, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    palabra = linea.strip().lower()
                    self.lista_excepciones.add(palabra)
        except FileNotFoundError:
            print(f"Error: El archivo {self.ruta_prohibidas} no se encontró.")
        except Exception as e:
            print(f"Error: No se pudo leer el archivo {self.ruta_prohibidas}: {e}")

    @staticmethod
    def limpiar_palabra(palabra):
        """
        Funcion que limpia las palabras, eliminando signos de puntuacion,
        caracteres especiales y convierte a minusculas
        """
        # Normaliza los caracteres Unicode
        palabra = ''.join(
            c for c in unicodedata.normalize('NFD', palabra)
            if unicodedata.category(c) != 'Mn'
        )
        # Elimina la puntuacion y convierte a minusculas
        palabra = re.sub(r'[^\w\s]', '', palabra)
        return palabra.lower()

    def procesar_texto(self):

        try:
            with open(self.ruta_texto, 'r', encoding='utf-8') as archivo:
                for linea in archivo:
                    palabras_listado = linea.split()
                    for palabra in palabras_listado:
                        palabra_purgada = self.limpiar_palabra(palabra)
                        if palabra_purgada and palabra_purgada not in self.lista_excepciones:
                            if palabra_purgada in self.frecuencia_palabra:
                                self.frecuencia_palabra[palabra_purgada] += 1
                            else:
                                self.frecuencia_palabra[palabra_purgada] = 1
        except FileNotFoundError:
            print(f"Error: El archivo {self.ruta_texto} no se encontró.")
        except Exception as e:
            print(f"Error al leer el archivo {self.ruta_texto}: {e}")

    def imprimir_frecuencias(self):

        # Muestra las frecuencias de las palabras en orden alfabetico
        for palabra in sorted(self.frecuencia_palabra.keys()):
            print(f"{palabra}: {self.frecuencia_palabra[palabra]}")

if __name__ == "__main__":
    contador = GestorPalabras('texto.in', 'prohibidas.in')
    contador.cargar_excepciones()
    contador.procesar_texto()
    contador.imprimir_frecuencias()
