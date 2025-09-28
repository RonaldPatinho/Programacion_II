class ValidarEntrada:
    @staticmethod
    # P2 Conversor a Glifos
    def validar_entrada(linea):
        """
        Valida que la entrada sea un numero entero en el rango 1 a 3999.
        """
        try:
            numero = int(linea.strip())
            if 1 <= numero <= 3999:
                return numero
            else:
                return None
        except ValueError:
            return None
