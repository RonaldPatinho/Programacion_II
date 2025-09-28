// bub js
class Game {
    constructor() {
        this.canvas = document.getElementById('canvas');
        this.ctx = this.canvas.getContext('2d');
        this.size = 10;
        this.cell = 40;
        this.colors = ['#f44', '#4f4', '#44f', '#ff4', '#f4f', '#4ff'];
        this.canvas.onclick = e => this.click(e);
        this.reset();
    }

    reset() {
        this.board = Array(this.size).fill().map(() => 
            Array(this.size).fill().map(() => 
                this.colors[Math.random() * 6 | 0]));
        this.score = 0;
        this.draw();
    }

    click(e) {
        const rect = this.canvas.getBoundingClientRect();
        const x = (e.clientX - rect.left) / this.cell | 0;
        const y = (e.clientY - rect.top) / this.cell | 0;
        
        const group = this.findGroup(x, y);
        if (group.length > 1) {
            this.score += group.length * (group.length - 1);
            group.forEach(([x, y]) => this.board[y][x] = null);
            this.collapse();
            this.draw();
            
            if (!this.hasGroups()) {
                alert(`Fin del juego! Puntaje: ${this.score}`);
                this.reset();
            }
        }
    }

    findGroup(x, y, color = this.board[y]?.[x], visited = new Set()) {
        if (!color || visited.has(`${x},${y}`)) return [];
        visited.add(`${x},${y}`);
        
        let group = [[x, y]];
        for (let [dx, dy] of [[0,1], [1,0], [0,-1], [-1,0]]) {
            const nx = x + dx, ny = y + dy;
            if (this.board[ny]?.[nx] === color && !visited.has(`${nx},${ny}`))
                group.push(...this.findGroup(nx, ny, color, visited));
        }
        return group;
    }

    collapse() {
        for (let x = 0; x < this.size; x++) {
            const col = [];
            for (let y = this.size - 1; y >= 0; y--)
                if (this.board[y][x]) col.push(this.board[y][x]);
            
            for (let y = 0; y < this.size; y++)
                this.board[y][x] = col[this.size - 1 - y] || null;
        }
    }

    hasGroups() {
        return this.board.some((row, y) => 
            row.some((cell, x) => cell && this.findGroup(x, y).length > 1));
    }

    draw() {
        this.ctx.clearRect(0, 0, 400, 400);
        for (let y = 0; y < this.size; y++) {
            for (let x = 0; x < this.size; x++) {
                if (this.board[y][x]) {
                    this.ctx.fillStyle = this.board[y][x];
                    this.ctx.beginPath();
                    this.ctx.arc(x * this.cell + 20, y * this.cell + 20, 18, 0, Math.PI * 2);
                    this.ctx.fill();
                }
            }
        }
        document.getElementById('score').textContent = `Puntaje: ${this.score}`;
    }
}

const game = new Game();