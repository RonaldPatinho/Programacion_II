// E1 Minas Script
class DetectorMinas {
    constructor() {
        this.filas = 0;
        this.columnas = 0;
        this.matriz = [];
        this.resultado = [];
    }

    esMina(matriz, i, j) {
        const md = matriz[i][j];
        let sumaVecinos = 0;
        let conteoVecinos = 0;

        for (let x = Math.max(0, i - 1); x <= Math.min(this.filas - 1, i + 1); x++) {
            for (let y = Math.max(0, j - 1); y <= Math.min(this.columnas - 1, j + 1); y++) {
                if (x !== i || y !== j) {
                    sumaVecinos += matriz[x][y];
                    conteoVecinos++;
                }
            }
        }

        const promedioVecinos = conteoVecinos > 0 ? sumaVecinos / conteoVecinos : 0;
        const total = md + promedioVecinos;
        console.log(`(Fila ${i + 1}, Columna ${j + 1}) -> MD: ${md}, Promedio Vecinos: ${promedioVecinos.toFixed(2)}, Total: ${total.toFixed(2)}`);
        return total > 40;
    }

    detectarMinas(matriz) {
        const resultado = Array(this.filas).fill().map(() => Array(this.columnas).fill(''));

        for (let i = 0; i < this.filas; i++) {
            for (let j = 0; j < this.columnas; j++) {
                if (this.esMina(matriz, i, j)) {
                    resultado[i][j] = '*';
                } else {
                    resultado[i][j] = ',';
                }
            }
        }

        this.resultado = resultado;
        return resultado;
    }

    mostrarEntrada(matriz) {
    const grid = document.getElementById('entradaGrid');
    grid.innerHTML = '';
    grid.style.gridTemplateColumns = `auto repeat(${this.columnas}, 30px)`;

    const emptyCell = document.createElement('div');
    emptyCell.className = 'cell label-cell';
    grid.appendChild(emptyCell);

    for (let j = 0; j < this.columnas; j++) {
        const label = document.createElement('div');
        label.className = 'cell label-cell';
        label.textContent = j + 1;
        grid.appendChild(label);
    }

    for (let i = 0; i < this.filas; i++) {
        const rowLabel = document.createElement('div');
        rowLabel.className = 'cell label-cell';
        rowLabel.textContent = i + 1;
        grid.appendChild(rowLabel);

        for (let j = 0; j < this.columnas; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = matriz[i][j];
            grid.appendChild(cell);
        }
    }
}

    mostrarSalida(resultado) {
    const grid = document.getElementById('salidaGrid');
    grid.innerHTML = '';
    grid.style.gridTemplateColumns = `auto repeat(${this.columnas}, 30px)`;

    const emptyCell = document.createElement('div');
    emptyCell.className = 'cell label-cell';
    grid.appendChild(emptyCell);

    for (let j = 0; j < this.columnas; j++) {
        const label = document.createElement('div');
        label.className = 'cell label-cell';
        label.textContent = j + 1;
        grid.appendChild(label);
    }

    for (let i = 0; i < this.filas; i++) {
        const rowLabel = document.createElement('div');
        rowLabel.className = 'cell label-cell';
        rowLabel.textContent = i + 1;
        grid.appendChild(rowLabel);

        for (let j = 0; j < this.columnas; j++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            cell.textContent = resultado[i][j];

            if (resultado[i][j] === '*') {
                cell.classList.add('mine-cell');
            } else {
                cell.style.color = 'white';
            }

            grid.appendChild(cell);
        }
    }
}
    generarArchivoSalida() {
        let contenido = '  ' + Array.from({ length: this.columnas }, (_, i) => i + 1).join(' ') + '\n';
        for (let i = 0; i < this.filas; i++) {
            contenido += `${i + 1} ` + this.resultado[i].join(' ') + '\n';
        }

        const blob = new Blob([contenido], { type: 'text/plain' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'minas.out';
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }
}

let detector;

function cargarArchivo() {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.in';
    input.onchange = (event) => {
        const file = event.target.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
            const contenido = e.target.result;
            procesarArchivo(contenido);
        };
        reader.readAsText(file);
    };
    input.click();
}

function procesarArchivo(contenido) {
    const lineas = contenido.split('\n').filter(linea => linea.trim() !== '');
    const [filas, columnas] = lineas[0].split(' ').map(Number);
    const matriz = lineas.slice(1, filas + 1).map(linea => linea.trim().split(' ').map(Number));

    detector = new DetectorMinas();
    detector.filas = filas;
    detector.columnas = columnas;

    const resultado = detector.detectarMinas(matriz);
    detector.mostrarEntrada(matriz);
    detector.mostrarSalida(resultado);

    document.getElementById('downloadButton').style.display = 'block';
}

function descargarArchivoSalida() {
    detector.generarArchivoSalida();
}
