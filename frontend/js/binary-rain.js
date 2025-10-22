// Binary Rain Effect
class BinaryRain {
    constructor(canvasId, opacity = 0.3) {
        this.canvas = document.getElementById(canvasId);
        if (!this.canvas) return;
        
        this.ctx = this.canvas.getContext('2d');
        this.opacity = opacity;
        this.chars = '01';
        this.fontSize = 20;
        this.columns = 0;
        this.drops = [];
        
        this.resizeCanvas();
        window.addEventListener('resize', () => this.resizeCanvas());
        
        this.startAnimation();
    }
    
    resizeCanvas() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.columns = Math.floor(this.canvas.width / this.fontSize);
        
        // Initialize drops
        this.drops = [];
        for (let i = 0; i < this.columns; i++) {
            this.drops[i] = Math.random() * this.canvas.height / this.fontSize;
        }
    }
    
    draw() {
        // Black background with slight transparency for trail effect
        this.ctx.fillStyle = 'rgba(0, 0, 0, 0.1)';
        this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.ctx.font = `${this.fontSize}px 'Courier New', monospace`;
        this.ctx.textAlign = 'left';
        
        for (let i = 0; i < this.drops.length; i++) {
            // Random binary character
            const text = this.chars[Math.floor(Math.random() * this.chars.length)];
            const x = i * this.fontSize;
            const y = this.drops[i] * this.fontSize;
            
            // Add opacity variation for depth - using light green colors
            const opacityVariation = Math.random() * 0.5 + 0.2;
            this.ctx.fillStyle = `rgba(144, 238, 144, ${opacityVariation})`;
            
            // Draw character
            this.ctx.fillText(text, x, y);
            
            // Reset drop when it reaches bottom or randomly
            if (y > this.canvas.height && Math.random() > 0.98) {
                this.drops[i] = 0;
            }
            
            // Move drop down slowly
            this.drops[i] += 0.5;
        }
    }
    
    startAnimation() {
        this.interval = setInterval(() => this.draw(), 100);
    }
    
    stop() {
        if (this.interval) {
            clearInterval(this.interval);
        }
    }
}

// Initialize binary rain when DOM is loaded
let binaryRainInstance = null;

function initBinaryRain() {
    // Create canvas if it doesn't exist
    if (!document.getElementById('binary-rain-canvas')) {
        const canvas = document.createElement('canvas');
        canvas.id = 'binary-rain-canvas';
        canvas.style.position = 'fixed';
        canvas.style.top = '0';
        canvas.style.left = '0';
        canvas.style.width = '100%';
        canvas.style.height = '100%';
        canvas.style.pointerEvents = 'none';
        canvas.style.zIndex = '1';
        document.body.insertBefore(canvas, document.body.firstChild);
    }
    
    binaryRainInstance = new BinaryRain('binary-rain-canvas', 0.3);
}

function stopBinaryRain() {
    if (binaryRainInstance) {
        binaryRainInstance.stop();
    }
}
