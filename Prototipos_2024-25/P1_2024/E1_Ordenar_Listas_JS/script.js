function asignarSigno(num) {
    return num.includes('-') ? parseInt(num) : parseInt(num);
}

function procesoDeOrdenamiento(lista) {
    const palabras = [];
    const numeros = [];
    lista.forEach(elemento => {
        if (/^-?\d+$/.test(elemento)) {
            numeros.push(elemento);
        } else {
            palabras.push(elemento);
        }
    });

    const numerosOrdenados = numeros.sort((a, b) => asignarSigno(a) - asignarSigno(b));
    const palabrasOrdenadas = palabras.sort((a, b) => a.localeCompare(b, undefined, { sensitivity: 'base' }));

    let indicePalabra = 0;
    let indiceNumero = 0;
    return lista.map(elemento => {
        if (/^-?\d+$/.test(elemento)) {
            return numerosOrdenados[indiceNumero++];
        } else {
            return palabrasOrdenadas[indicePalabra++];
        }
    });
}

function procesarArchivo(contenido) {
    const lineas = contenido.split('\n');
    const salida = [];
    lineas.forEach(linea => {
        if (linea.trim() === '.') {
            salida.push(linea.trim());
            return;
        }
        const elementos = linea.trim().replace(/\.$/, '').split(', ');
        const listaOrdenada = procesoDeOrdenamiento(elementos);
        salida.push(listaOrdenada.join(', ') + '.');
    });
    return salida.join('\n');
}

function seleccionarArchivo() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.in';
    input.onchange = (event) => {
        const archivo = event.target.files[0];
        if (!archivo) return;

        const lector = new FileReader();
        lector.onload = (e) => {
            const contenido = e.target.result;
            document.getElementById('entradaText').value = contenido;
            const salida = procesarArchivo(contenido);
            document.getElementById('salidaText').value = salida;

            const blob = new Blob([salida], { type: 'text/plain' });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = 'Salida.out';
            document.body.appendChild(a);
            a.click();
            document.body.removeChild(a);
        };
        lector.readAsText(archivo);
    };
    input.click();
}
