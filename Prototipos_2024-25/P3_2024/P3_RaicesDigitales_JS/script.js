function leerLineas(contenido) {
    return contenido.split('\n').map(linea => linea.trim()).filter(linea => linea !== '');
}

function raizDigital(numero) {
    while (numero >= 10) {
        let suma = 0;
        let num = numero;
        while (num > 0) {
            suma += num % 10;
            num = Math.floor(num / 10);
        }
        numero = suma;
    }
    return numero;
}

function calcularYMostrar() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt';
    input.onchange = (event) => {
        const archivo = event.target.files[0];
        if (!archivo) return;

        const lector = new FileReader();
        lector.onload = (e) => {
            const contenido = e.target.result;
            const lineas = leerLineas(contenido);
            const resultados = [];
            lineas.forEach(linea => {
                const numero = parseInt(linea, 10);
                if (isNaN(numero)) {
                    console.error(`Error al convertir la información en un número: ${linea}`);
                    return;
                }
                if (numero === 0) return;
                const raiz = raizDigital(numero);
                resultados.push(`Raíz digital de ${numero} es ${raiz}`);
            });
            document.getElementById('resultado').textContent = resultados.join('\n');
        };
        lector.readAsText(archivo);
    };
    input.click();
}
