class RompeBurbujas {
    constructor() {
        this.canvas = document.getElementById('gameCanvas');
        this.ctx = this.canvas.getContext('2d');
        this.filas = this.columnas = 10;
        this.tamano = 50;
        this.colores = ["#ff6b6b", "#4ecdc4", "#6aa84f", "#f9ca24", "#6c5ce7", "#fd79a8"];
        this.puntaje = 0;
        this.canvas.onclick = (e) => this.clic(e);
        this.nuevoJuego();
    }

    generarTablero() {
        return Array(this.filas).fill().map(() => 
            Array(this.columnas).fill().map(() => 
                this.colores[Math.floor(Math.random() * this.colores.length)]));
    }

    encontrarGrupo(f, c) {
        const color = this.tablero[f]?.[c];
        if (!color) return [];
        
        const visitados = new Set();
        const grupo = [[f, c]];
        
        for (let [f, c] of grupo) {
            const key = `${f},${c}`;
            if (visitados.has(key)) continue;
            visitados.add(key);
            
            for (let [df, dc] of [[0,1], [1,0], [0,-1], [-1,0]]) {
                const [nf, nc] = [f + df, c + dc];
                if (nf >= 0 && nf < this.filas && nc >= 0 && nc < this.columnas && 
                    this.tablero[nf][nc] === color && !visitados.has(`${nf},${nc}`)) {
                    grupo.push([nf, nc]);
                }
            }
        }
        return grupo.length > 1 ? grupo : [];
    }

    eliminarGrupo(grupo) {
        grupo.forEach(([f, c]) => this.tablero[f][c] = null);
        
        // Colapsar columnas
        for (let c = 0; c < this.columnas; c++) {
            const col = this.tablero.map(fila => fila[c]).filter(Boolean);
            for (let f = 0; f < this.filas; f++) {
                this.tablero[f][c] = f >= this.filas - col.length ? 
                    col[f - (this.filas - col.length)] : null;
            }
        }
    }

    dibujar() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        for (let f = 0; f < this.filas; f++) {
            for (let c = 0; c < this.columnas; c++) {
                if (this.tablero[f][c]) {
                    const [x, y] = [c * this.tamano, f * this.tamano];
                    
                    // Burbuja principal
                    this.ctx.fillStyle = this.tablero[f][c];
                    this.ctx.strokeStyle = '#6272a4';
                    this.ctx.lineWidth = 2;
                    this.ctx.beginPath();
                    this.ctx.arc(x + 25, y + 25, 23, 0, Math.PI * 2);
                    this.ctx.fill();
                    this.ctx.stroke();
                    
                    // Brillo
                    const gradient = this.ctx.createRadialGradient(x + 15, y + 15, 0, x + 15, y + 15, 8);
                    gradient.addColorStop(0, 'rgba(255,255,255,0.6)');
                    gradient.addColorStop(1, 'rgba(255,255,255,0.1)');
                    this.ctx.fillStyle = gradient;
                    this.ctx.beginPath();
                    this.ctx.arc(x + 15, y + 15, 8, 0, Math.PI * 2);
                    this.ctx.fill();
                }
            }
        }
    }

    clic(e) {
        const rect = this.canvas.getBoundingClientRect();
        const [x, y] = [e.clientX - rect.left, e.clientY - rect.top];
        const [f, c] = [Math.floor(y / this.tamano), Math.floor(x / this.tamano)];
        
        const grupo = this.encontrarGrupo(f, c);
        if (grupo.length > 0) {
            this.puntaje += grupo.length * (grupo.length - 1);
            this.eliminarGrupo(grupo);
            this.dibujar();
            document.getElementById('score').textContent = `Puntaje: ${this.puntaje}`;
            
            // Verificar fin del juego
            if (!this.tablero.some((fila, f) => 
                fila.some((celda, c) => celda && this.encontrarGrupo(f, c).length > 0))) {
                setTimeout(() => {
                    alert(`🎉 ¡Fin del juego!\nPuntaje final: ${this.puntaje}\n¡Bien jugado!`);
                    this.nuevoJuego();
                }, 100);
            }
        }
    }

    nuevoJuego() {
        this.tablero = this.generarTablero();
        this.puntaje = 0;
        document.getElementById('score').textContent = 'Puntaje: 0';
        this.dibujar();
    }
}

const game = new RompeBurbujas();