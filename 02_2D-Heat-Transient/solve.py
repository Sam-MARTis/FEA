import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Constants
Lx = 1.0  # Length of the domain in x
Ly = 1.0  # Length of the domain in y
Nx = 50  # Number of grid points in x
Ny = 50  # Number of grid points in y
dx = Lx / (Nx - 1)
dy = Ly / (Ny - 1)
alpha = 1e-4  # Thermal diffusivity (alpha = k/(rho*c))
dt = 0.01  # Time step
Nt = 10000  # Number of time steps

# Initial temperature distribution
T = np.zeros((Nx, Ny))
T[int(Nx / 2), int(Ny / 2)] = 100  # Initial heat source in the center

# Boundary conditions (constant temperature)
T[:, 0] = 0  # Left
T[:, -1] = 0  # Right
T[0, :] = 0  # Top
T[-1, :] = 0  # Bottom

# Function to perform one time step using finite difference method
def update_temperature(T, alpha, dt, dx, dy):
    T_new = T.copy()
    for i in range(1, Nx-1):
        for j in range(1, Ny-1):
            T_new[i, j] = T[i, j] + alpha * dt * (
                (T[i+1, j] - 2*T[i, j] + T[i-1, j]) / dx**2 +
                (T[i, j+1] - 2*T[i, j] + T[i, j-1]) / dy**2
            )
    return T_new

# Set up the figure and axis for plotting
fig, ax = plt.subplots()
cax = ax.imshow(T, cmap='hot', origin='lower', extent=[0, Lx, 0, Ly])
fig.colorbar(cax)

# Animation update function
def animate(n):
    global T
    for i in range(1000):
        T[int(Nx / 2), int(Ny / 2)] = 100 
        T = update_temperature(T, alpha, dt, dx, dy)    
    cax.set_array(T)
    return [cax]

# Create animation
anim = FuncAnimation(fig, animate, frames=Nt, interval=5, blit=True)

# Display the animation
plt.show()
