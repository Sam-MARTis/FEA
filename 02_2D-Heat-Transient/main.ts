const canvas = document.getElementById("projectCanvas") as HTMLCanvasElement;
canvas.width = window.innerWidth * devicePixelRatio;
canvas.height = window.innerHeight * devicePixelRatio;
const ctx = canvas.getContext("2d") as CanvasRenderingContext2D;
if (ctx === null) {
  throw new Error("Canvas not supported");
}

// Defining Hyperparameters first

const dt = 0.00001; //Remember, dt/dx^2 < 0.5 for stability. keep it <0.1 for safety
const dx = 0.01;
const dy = 0.01;
const X = 1;
const Y = 1;
const SCALE_TO_PIXEL = 5;

const No_X = Math.floor(X / dx);
const No_Y = Math.floor(Y / dy);

// Defining the grid
const grid = new Array(No_Y).fill(0).map(() => new Array(No_X).fill(100)); // Y vertical, X horizontal

//Core functions
const enforceBoundaryConditions = (grid: number[][]) => {
  for (let y = 0; y < grid.length; y++) {
    grid[y][0] = 0;
    grid[y][grid[0].length - 1] = 250;
  }
  // for(let x=0; x<X; x++){
  //     // grid[0][x] = 0;
  //     // grid[Y-1][x] = 250;
  // }
  for (let xi = -2; xi < 2; xi++) {
    for (let yi = -2; yi < 2; yi++) {
      grid[xi+Math.floor((grid.length - 1) / 2)][
        Math.floor(yi + (grid[0].length - 1) / 2)
      ] = 250;
    }
  }
  grid[Math.floor((grid.length - 1) / 2)][10+Math.floor((grid[0].length - 1) / 2)] = 0;

};


const calculateLaplacian = (grid: number[][], y:number, x:number): number => {
  let countx = 0;
  let county = 0;
  let laplacian = 0;
  if(y!=0){
    county++;
    laplacian += grid[y-1][x]/(dy*dy);
  }
  if(y!=No_Y-1){
    county++;
    laplacian += grid[y+1][x]/(dy*dy);
  }
  if(x!=0){
    countx++;
    laplacian += grid[y][x-1]/(dx*dx);
  }
  if(x!=No_X-1){
    countx++;
    laplacian += grid[y][x+1]/(dx*dx);
  }
  laplacian = (laplacian - ((countx*grid[y][x]/(dx*dx)) + (county*grid[y][x]/(dy*dy))));
  return laplacian;
};
const updateFT = (grid: number[][]) => {
  enforceBoundaryConditions(grid);
  for (let y = 0; y < No_Y; y++) {
    for (let x = 0; x < No_X; x++) {
      grid[y][x] = grid[y][x] + dt * calculateLaplacian(grid, y, x);
    }
  }



};
const updateLeapFrog = (grid: number[][], grid2: number[][], switcher:boolean) => {
  enforceBoundaryConditions(grid);
  for (let y = 0; y < No_Y; y++) {
    for (let x = 0; x < No_X; x++) {
      grid[y][x] = grid[y][x] + 2 * dt * calculateLaplacian(grid, y, x);
    }
  }

  // Top and bottom are free ends. Laplacian calculation ensueres adiabatic boundary conditions


}

// Display function
const display = (grid: number[][], ctx: CanvasRenderingContext2D) => {
  for (let y = 0; y < No_Y; y++) {
    for (let x = 0; x < No_X; x++) {
      ctx.fillStyle = `rgb(${grid[y][x]},${grid[y][x] / 3},${
        255 - grid[y][x]
      })`;
      ctx.fillRect(
        x * SCALE_TO_PIXEL,
        y * SCALE_TO_PIXEL,
        SCALE_TO_PIXEL,
        SCALE_TO_PIXEL
      );
    }
  }
};

// Update function

// Animation loop
function animate() {
  display(grid, ctx);
  updateFT(grid);
  requestAnimationFrame(animate);

}

animate();
