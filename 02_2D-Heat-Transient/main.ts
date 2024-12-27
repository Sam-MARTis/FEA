
const canvas = document.getElementById("projectCanvas") as HTMLCanvasElement;
canvas.width = window.innerWidth*devicePixelRatio;
canvas.height = window.innerHeight*devicePixelRatio;
const ctx = canvas.getContext("2d") as CanvasRenderingContext2D;
if(ctx === null){
    throw new Error("Canvas not supported");
}


// Defining Hyperparameters first

const dt= 0.003;
const dx= 0.1;
const dy= 0.1;
const X = 10;
const Y = 10;
const SCALE_TO_PIXEL = 30;

// Defining the grid
const grid = new Array(Y).fill(0).map(() => new Array(X).fill(100)); // Y vertical, X horizontal


// Display function
function display(grid: number[][], ctx: CanvasRenderingContext2D){
    for(let y=0; y<Y; y++){
        for(let x=0; x<X; x++){
            ctx.fillStyle = `rgb(${grid[y][x]},${grid[y][x]},${grid[y][x]})`;
            ctx.fillRect(x*SCALE_TO_PIXEL, y*SCALE_TO_PIXEL, SCALE_TO_PIXEL, SCALE_TO_PIXEL);
        }
    }
}

// Update function


// Animation loop
function animate(){
    display(grid, ctx);
    requestAnimationFrame(animate);
}