class ConversorAGlifo:
    def __init__(self):
        # P2 Conversor a Glifos
        """
        Diccionario para establecer el valor de cada simbolo
        """
        self.glifos = [
            ('Σ', 1),('Λ', 5),
            ('Ω', 10), ('Δ', 50),
            ('Φ', 100),('Ψ', 500),
            ('Ξ', 1000)
        ]

        # Combinaciones sustractivas
        self.combinaciones_sustractivas = {
            'ΣΛ': 4,'ΣΩ': 9,'ΛΩ': 5,
            'ΩΔ': 40,'ΩΦ': 90,'ΔΦ': 50,
            'ΦΨ': 400,'ΦΞ': 900
        }

        # Orden de los glifos para la representacion canonica
        self.orden_glifos = ['Ξ', 'Ψ', 'Φ', 'Δ', 'Ω', 'Λ', 'Σ']

    def convertir_a_glifos(self, numero):
        """ Metodo que hace la conversion de numero a glifo y expresion canonica.
        Retorna una cadena con los glifos."""

        # Primero intenta con Greedy
        resultado_greedy = self._convertir_greedy(numero)

        # Verifica si hay una combinacion mas corta, usa fuerza bruta
        resultado_bruta = self._convertir_fuerza_bruta_limitada(numero)

        # Seleccionamos el resultado mas corto
        if len(resultado_bruta) < len(resultado_greedy):
            return resultado_bruta
        return resultado_greedy

    def _convertir_greedy(self, numero):
        """Algoritmo greedy para encontrar una solucion funcional"""
        resultado = []

        # Primero usa las combinaciones sustractivas mas grandes
        for comb, val in sorted(self.combinaciones_sustractivas.items(), key=lambda x: -x[1]):
            while numero >= val:
                resultado.append(comb)
                numero -= val
                if numero == 0:
                    return ''.join(resultado)

        # Luego un bucle para glifos individuales
        for glifo in self.orden_glifos:
            valor = self._obtener_valor_glifo(glifo)
            while numero >= valor:
                # Verifica las repeticiones
                if len(resultado) >= 3 and resultado[-1] == resultado[-2] == resultado[-3] == glifo:
                    for comb, val in self.combinaciones_sustractivas.items():
                        if comb[1] == glifo and numero + valor >= val:
                            resultado = resultado[:-3]
                            resultado.append(comb)
                            numero = numero + valor - val
                            break
                    else:
                        resultado.append(glifo)
                        numero -= valor
                else:
                    resultado.append(glifo)
                    numero -= valor

        return ''.join(resultado)

    def _convertir_fuerza_bruta_limitada(self, numero):
        """ Metodo de fuerza bruta para verificar si hay una solucion mas corta"""
        # Se limita la profundidad de busqueda para evitar desbordamiento
        profundidad_max = 20
        pila = [([], numero, 0)]
        mejores_resultados = []

        while pila and len(mejores_resultados) < 5:
            actual, num_restante, profundidad = pila.pop()

            if num_restante == 0:
                resultado_str = ''.join(actual)
                if resultado_str:
                    mejores_resultados.append((resultado_str, len(resultado_str)))
                continue

            if profundidad >= profundidad_max:
                continue

            for comb, val in self.combinaciones_sustractivas.items():
                if num_restante >= val:
                    pila.append((actual + [comb], num_restante - val, profundidad + 1))

            for glifo, val in self.glifos:
                if num_restante >= val:
                    pila.append((actual + [glifo], num_restante - val, profundidad + 1))

        # Seleccionar la combinaciin mas corta
        if mejores_resultados:
            mejores_resultados.sort(key=lambda x: len(x[0]))
            return mejores_resultados[0][0]
        return ""

    def _obtener_valor_glifo(self, glifo):
        for g, v in self.glifos:
            if g == glifo:
                return v
        return 0