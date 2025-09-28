class Adyacente {
    constructor(id_destino, costo, siguiente = null) {
        this.id_destino = id_destino;
        this.costo = costo;
        this.siguiente_adyacente = siguiente;
    }
}
// Grafo dirigido y ponderado
class Grafo {
    constructor() {
        this.listas_adyacencia = {};
    }

    agregarArista(origen, destino, costo) {
        this.listas_adyacencia[origen] = new Adyacente(destino, costo, this.listas_adyacencia[origen]);
    }

    obtenerAdyacentes(estacion) {
        let adyacentes = [];
        let actual = this.listas_adyacencia[estacion];
        while (actual) {
            adyacentes.push([actual.id_destino, actual.costo]);
            actual = actual.siguiente_adyacente;
        }
        return adyacentes;
    }

    obtenerEstaciones() {
        const estaciones = new Set();
        Object.keys(this.listas_adyacencia).forEach(origen => {
            const numOrigen = parseInt(origen);
            estaciones.add(numOrigen);
            this.obtenerAdyacentes(numOrigen).forEach(([destino]) => estaciones.add(destino));
        });
        return Array.from(estaciones);
    }

    mostrarRed() {
        return "Red de transporte:\n" +
            Object.keys(this.listas_adyacencia).map(Number).sort((a, b) => a - b)
            .map(estacion => `Estación ${estacion}: ${JSON.stringify(this.obtenerAdyacentes(estacion))}`)
            .join('\n');
    }
}

class ColaPrioridad {
    constructor() {
        this.elementos = [];
    }

    insertar(elemento) {
        this.elementos.push(elemento);
        this.elementos.sort((a, b) => a[0] - b[0]);
    }

    extraerMinimo() {
        return this.elementos.shift();
    }

    estaVacia() {
        return this.elementos.length === 0;
    }
}

function cargarRedDesdeArchivo(contenidoArchivo) {
    const grafo = new Grafo();
    const lineas = contenidoArchivo.split('\n').filter(linea => linea.trim() !== '');
    if (lineas.length === 0) return null;

    const [N, M] = lineas[0].trim().split(/\s+/).map(Number);
    for (let i = 1; i <= M; i++) {
        if (i < lineas.length) {
            const [origen, destino, costo] = lineas[i].trim().split(/\s+/).map(Number);
            grafo.agregarArista(origen, destino, costo);
        }
    }
    return grafo;
}

function dijkstra(grafo, origen, destino) {
    const estaciones = grafo.obtenerEstaciones();
    if (!estaciones.includes(origen) || !estaciones.includes(destino)) return [[], Infinity];

    const distancias = {}, previos = {};
    estaciones.forEach(estacion => {
        distancias[estacion] = Infinity;
        previos[estacion] = null;
    });
    distancias[origen] = 0;

    const colaPrioridad = new ColaPrioridad();
    colaPrioridad.insertar([0, origen]);

    while (!colaPrioridad.estaVacia()) {
        const [distanciaActual, estacionActual] = colaPrioridad.extraerMinimo();
        if (distanciaActual > distancias[estacionActual]) continue;

        grafo.obtenerAdyacentes(estacionActual).forEach(([destinoAdyacente, costo]) => {
            const nuevaDistancia = distanciaActual + costo;
            if (nuevaDistancia < distancias[destinoAdyacente]) {
                distancias[destinoAdyacente] = nuevaDistancia;
                previos[destinoAdyacente] = estacionActual;
                colaPrioridad.insertar([nuevaDistancia, destinoAdyacente]);
            }
        });
    }

    if (distancias[destino] === Infinity) return [[], Infinity];

    let nodoActual = destino, camino = [];
    while (nodoActual !== null) {
        camino.push(nodoActual);
        nodoActual = previos[nodoActual];
    }
    camino.reverse();

    const rutaDetallada = camino.slice(0, -1).map((origenCamino, i) => {
        const destinoCamino = camino[i + 1];
        const costo = grafo.obtenerAdyacentes(origenCamino).find(([dest]) => dest === destinoCamino)?.[1];
        return [origenCamino, destinoCamino, costo];
    });

    return [rutaDetallada, distancias[destino]];
}
