function leerArchivo(contenido) {
    const lineas = contenido.split('\n');
    const tiempos = [];
    for (const linea of lineas) {
        const partes = linea.trim().split(/\s+/);
        if (partes.length === 4) {
            const [horaInicio, minutoInicio, horaFin, minutoFin] = partes.map(Number);
            tiempos.push([horaInicio, minutoInicio, horaFin, minutoFin]);
        } else {
            alert("El archivo de entrada no cumple con los parámetros establecidos.");
            return [];
        }
    }
    return tiempos;
}

function contarCrucesHoras(horaInicio, minutoInicio, horaFin, minutoFin) {
    let tiempoInicioTotal = horaInicio * 60 + minutoInicio;
    let tiempoFinTotal = horaFin * 60 + minutoFin;
    if (tiempoFinTotal <= tiempoInicioTotal) {
        tiempoFinTotal += 12 * 60;
    }

    let intervalosTiempo = 0;
    const anguloMinuto = 360 / 60;
    const anguloHora = 360 / 12 / 60;
    let anguloHoraActual = (horaInicio % 12) * 30 + minutoInicio * 0.5;
    let anguloMinutoActual = minutoInicio * anguloMinuto;
    let anguloHoraAnterior = anguloHoraActual;
    let anguloMinutoAnterior = anguloMinutoActual;

    for (let i = tiempoInicioTotal; i < tiempoFinTotal; i++) {
        anguloHoraActual += anguloHora;
        anguloMinutoActual += anguloMinuto;
        if (anguloHoraActual >= 360) {
            anguloHoraActual -= 360;
        }
        if (anguloMinutoActual >= 360) {
            anguloMinutoActual -= 360;
        }
        if ((anguloMinutoAnterior <= anguloHoraAnterior && anguloHoraAnterior < anguloMinutoActual) ||
            (anguloMinutoAnterior < anguloHoraActual && anguloHoraActual <= anguloMinutoActual)) {
            intervalosTiempo++;
        }
        anguloHoraAnterior = anguloHoraActual;
        anguloMinutoAnterior = anguloMinutoActual;
    }
    return intervalosTiempo;
}

function cargarArchivo() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.in';
    input.onchange = (event) => {
        const archivo = event.target.files[0];
        if (!archivo) return;

        const lector = new FileReader();
        lector.onload = (e) => {
            const contenido = e.target.result;
            const tiempos = leerArchivo(contenido);
            mostrarResultados(tiempos);
        };
        lector.readAsText(archivo);
    };
    input.click();
}

function mostrarResultados(tiempos) {
    const tbody = document.querySelector('#resultTable tbody');
    tbody.innerHTML = '';
    tiempos.forEach(([horaInicio, minutoInicio, horaFin, minutoFin]) => {
        const cruces = contarCrucesHoras(horaInicio, minutoInicio, horaFin, minutoFin);
        const fila = document.createElement('tr');
        fila.innerHTML = `
            <td>${String(horaInicio).padStart(2, '0')}:${String(minutoInicio).padStart(2, '0')}</td>
            <td>${String(horaFin).padStart(2, '0')}:${String(minutoFin).padStart(2, '0')}</td>
            <td>${cruces}</td>
        `;
        tbody.appendChild(fila);
    });
}
