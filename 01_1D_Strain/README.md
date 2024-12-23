# FEM for static strain analysis

## Aim
To undertsnad how FEA works to build more complicated stuff.

Static analysis is performed to calculate strain.


## Steps
First, the hyperparamters are decided. U_specified are fixed displacements. Essential Boundary conditions are encoded here.

Natural Boundary conditions are encoded in the Q_specified dictionary.
```python
NUMBER_OF_ELEMENTS = 1000
BAR_LENGTH = 10
FORCE_CONSTANT = 3
E = 100000
A = 1

he = BAR_LENGTH / NUMBER_OF_ELEMENTS
U_SPECIFIED = {0: 0, BAR_LENGTH: 0}
Q_SPECIFIED = {} #0 by default
def force_function(x): #Distributed force
    return FORCE_CONSTANT*x


```



We then construct the connectivity and element stiffness matrix.

We use linear first order shape functions to describe our displacement field.
```python
connectivity_matrix = []

for i in range(NUMBER_OF_ELEMENTS):
    connectivity_matrix.append([i, i+1])
element_stiffness_matrix = [[E*A/he, -E*A/he], [-E*A/he, E*A/he]]
```

Here, the element stiffness matrix is precomputed but it need not be the case for arbitrary shape functions.

We then assemble the global stiffness matrix using the connectivity matrix.
```python
for i in range(NUMBER_OF_ELEMENTS):
    for j in range(2):
        for k in range(2):
            global_stiffness_matrix[connectivity_matrix[i][j]][connectivity_matrix[i][k]] += element_stiffness_matrix[j][k]
```


The Lagrangian shape functions are also used as the weight functions (Galerkin method) and the force vector is assembled.

```python
def shape_function(x, i):
    if i == 0:
        return 1 - (x%he)/he
    elif i == 1:
        return (x%he)/he
    
def element_force_distributed(i):
    return [integrate(lambda x: force_function(x)*shape_function(x, 0), i*he, (i+1)*he), integrate(lambda x: force_function(x)*shape_function(x, 1), i*he, (i+1)*he)]

distributed_force = [0 for i in range(NUMBER_OF_ELEMENTS+1)]
for i in range(NUMBER_OF_ELEMENTS):
    force = element_force_distributed(i)
    for j in range(2):
        distributed_force[connectivity_matrix[i][j]] += force[j]
```


The global stiffness matrix is non-onvertible. However, since we know some of the inputs (U_specified), we can break the matrix into sub-matrices that are solveable.

$$[K] = \begin{bmatrix}
K_{11} \ \ \ K_{12}\\ 
K_{21} \ \ \ K_{22}
\end{bmatrix}$$

We split it in such a way that we can solve for the unknown U values

$$\begin{bmatrix}
K_{11} \ |\ \ K_{12}\\ 
--- --\\
K_{21} \  |\ \ K_{22}
\end{bmatrix} \begin{pmatrix}
U_{known} \\
--- \\
U_{unknown}
\end{pmatrix} = \begin{pmatrix}F_{known} \\
--- \\
F_{unknown}
\end{pmatrix}$$


$$U_{unknown} = K_{22}^{-1}(F_{known} - K_{21}U_{known})$$
Since RHS is comprised of known quanities, LHS can be obtained



```python
K11 = global_stiffness_matrix[:no_u_specified, :no_u_specified]
K12 = global_stiffness_matrix[:no_u_specified, no_u_specified:]
K21 = global_stiffness_matrix[no_u_specified:, :no_u_specified]
K22 = global_stiffness_matrix[no_u_specified:, no_u_specified:]
U_known = U[:no_u_specified]
U_unknown = U[no_u_specified:]


Q_known = distributed_force[no_u_specified:]
Q_unknown = distributed_force[:no_u_specified]

K22_inv = np.linalg.inv(K22)
U_unknown_found = np.matvec(K22_inv, Q_known - np.matvec(K21, U_known))
```

E-100000_A-1_FORCE-CONSTANT-3_F=Kx_Length-10_Number_of_elements-1000_U-{0: 0, 10: 0}_Q-{}
![E-100000_A-1_FORCE-CONSTANT-3_F=Kx_Length-10_Number_of_elements-1000_U-{0: 0, 10: 0}_Q-{}](</01_1D_Strain/E-100000_A-1_FORCE-CONSTANT-3_F=Kx_Length-10_Number_of_elements-1000_U-{0: 0, 10: 0}_Q-{}.png?raw=true>)
