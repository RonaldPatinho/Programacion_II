let grafo = null;
let contenidoDescarga = "";
// Elementos del DOM
const fileInput = document.getElementById('file-input');
const fileNameSpan = document.getElementById('file-name');
const mostrarRedBtn = document.getElementById('mostrar-red');
const calcularRutaBtn = document.getElementById('calcular-ruta');
const salirBtn = document.getElementById('salir');
const salidaDiv = document.getElementById('salida');
const modalRuta = document.getElementById('modal-ruta');
const closeModal = document.querySelector('#modal-ruta .close');
const calcularBtn = document.getElementById('calcular-btn');
const descargarBtn = document.getElementById('descargar-btn');

function descargarArchivo(contenido, nombreArchivo) {
    const blob = new Blob([contenido], { type: 'text/plain' });
    const enlace = document.createElement('a');
    enlace.href = URL.createObjectURL(blob);
    enlace.download = nombreArchivo;
    document.body.appendChild(enlace);
    enlace.click();
    setTimeout(() => {
        document.body.removeChild(enlace);
        URL.revokeObjectURL(enlace.href);
    }, 100);
}

descargarBtn.addEventListener('click', function() {
    if (contenidoDescarga) {
        descargarArchivo(contenidoDescarga, 'rutas_optimas.txt');
    } else {
        alert("No hay contenido para descargar. Por favor, calcula una ruta óptima primero.");
    }
});

fileInput.addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file) return;

    fileNameSpan.textContent = file.name;

    const reader = new FileReader();
    reader.onload = function(e) {
        const contenido = e.target.result;
        grafo = cargarRedDesdeArchivo(contenido);
        salidaDiv.textContent = grafo ? "Archivo cargado correctamente." : "Error al cargar el archivo.";
    };
    reader.readAsText(file);
});

mostrarRedBtn.addEventListener('click', function() {
    if (!grafo) {
        salidaDiv.textContent = "Por favor, carga primero un archivo.";
        return;
    }
    salidaDiv.textContent = grafo.mostrarRed();
    descargarBtn.style.display = 'none';
});

calcularRutaBtn.addEventListener('click', function() {
    if (!grafo) {
        salidaDiv.textContent = "Por favor, carga primero un archivo.";
        return;
    }
    modalRuta.style.display = 'block';
});

closeModal.addEventListener('click', function() {
    modalRuta.style.display = 'none';
});

calcularBtn.addEventListener('click', function() {
    const origen = parseInt(document.getElementById('origen').value);
    const destino = parseInt(document.getElementById('destino').value);

    if (isNaN(origen) || isNaN(destino)) {
        alert("Por favor ingrese números enteros válidos para las estaciones.");
        return;
    }

    const [ruta, costoTotal] = dijkstra(grafo, origen, destino);

    let salidaTexto = '';
    if (costoTotal === Infinity) {
        salidaTexto = `No hay ruta posible desde ${origen} a ${destino}.`;
    } else {
        salidaTexto = `La ruta óptima de ${origen} a ${destino} es:\n` +
            ruta.map(([o, d, c]) => `Estación ${o} -> Estación ${d} (Costo: ${c})`).join('\n') +
            `\nCosto total de la ruta: ${costoTotal}`;
    }

    salidaDiv.textContent = salidaTexto;
    contenidoDescarga = salidaTexto;
    descargarBtn.style.display = 'block';
    modalRuta.style.display = 'none';
});

salirBtn.addEventListener('click', function() {
    if (confirm("¿Seguro de querer salir?")) {
        window.close();
    }
});

window.addEventListener('click', function(event) {
    if (event.target === modalRuta) {
        modalRuta.style.display = 'none';
    }
});
