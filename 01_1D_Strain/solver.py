import numpy as np
import matplotlib.pyplot as plt

from swap import swap_full


#Hyperparameters
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







no_u_specified = len(U_SPECIFIED.keys())
no_q_explicitly_specified = len(Q_SPECIFIED.keys())
if NUMBER_OF_ELEMENTS + 1 - no_q_explicitly_specified < no_u_specified:
    raise Exception("Overconstrained system")

no_q_specified =  NUMBER_OF_ELEMENTS + 1 - no_u_specified

q_essential = dict()
u_essential = dict()
for i in U_SPECIFIED.keys():
    eVal = np.round(i/he)
    u_essential[eVal] = U_SPECIFIED[i]
for i in Q_SPECIFIED.keys():
    eVal = np.round(i/he)
    q_essential[eVal] = Q_SPECIFIED[i]



connectivity_matrix = []

for i in range(NUMBER_OF_ELEMENTS):
    connectivity_matrix.append([i, i+1])

# print(connectivity_matrix)
element_stiffness_matrix = [[E*A/he, -E*A/he], [-E*A/he, E*A/he]]

global_stiffness_matrix = [[0 for i in range(NUMBER_OF_ELEMENTS+1)] for j in range(NUMBER_OF_ELEMENTS+1)]

for i in range(NUMBER_OF_ELEMENTS):
    for j in range(2):
        for k in range(2):
            global_stiffness_matrix[connectivity_matrix[i][j]][connectivity_matrix[i][k]] += element_stiffness_matrix[j][k]

# print(global_stiffness_matrix)


def integrate(f, a, b):
    n = 1000
    h = (b-a)/n
    s = 0.5*(f(a) + f(b))
    for i in range(1, n):
        s += f(a + i*h)
    return s*h

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

global_stiffness_matrix = np.array(global_stiffness_matrix)
distributed_force = np.array(distributed_force)
for i in q_essential.keys():
    print(int(i))
    distributed_force[int(i)] += q_essential[i]


#Construct U
U = np.array([None for i in range(NUMBER_OF_ELEMENTS+1)])
for i in u_essential.keys():
    U[int(i)] = u_essential[i]
# U_known = np.array([u_essential[i] for i in u_essential.keys()])

# Now I need to swap known stuff to make matrix invertible
reference_vector = np.array([i for i in range(NUMBER_OF_ELEMENTS+1)])

def swap_positions(matrix:np.array, input_vector, output_vector, reference_vector):
    for index_to_switch_to, index_with_u_specified in enumerate(u_essential.keys()):
        # print(index_with_u_specified, index_to_switch_to)
        swap_full(matrix, input_vector, output_vector,int(index_with_u_specified), index_to_switch_to, reference_vector)

swap_positions(global_stiffness_matrix, distributed_force, U, reference_vector)





#Swapping is done so now I need to split the stiffness matrix and vectors.
K11 = global_stiffness_matrix[:no_u_specified, :no_u_specified]
K12 = global_stiffness_matrix[:no_u_specified, no_u_specified:]
K21 = global_stiffness_matrix[no_u_specified:, :no_u_specified]
K22 = global_stiffness_matrix[no_u_specified:, no_u_specified:]

print("size of K11", K11.shape)
print("size of K12", K12.shape)
print("size of K21", K21.shape)
print("size of K22", K22.shape)


U_known = U[:no_u_specified]
U_unknown = U[no_u_specified:]


Q_known = distributed_force[no_u_specified:]
Q_unknown = distributed_force[:no_u_specified]




print("Reference vector", reference_vector)
#Solve
K22_inv = np.linalg.inv(K22)
# print("Known extension effect", np.matvec(K21, U_known))
print("K22", K22)
print("K22_inv", K22_inv)
U_unknown_found = np.matvec(K22_inv, Q_known - np.matvec(K21, U_known))
print("U_unkown_found: ", U_unknown_found)
print()
print("Q predicted:", np.matvec(K22, U_unknown_found))
print("Q known:", Q_known)

# U_unknown_found = np.linalg.solve(K22, Q_known - np.dot(K21, U_known))
# print()
# print(U_unknown_found)
# print()

# Post processing
dU = np.zeros(len(U_unknown_found))
for i in range(1, len(U_unknown_found)):
    dU[i] = U_unknown_found[i] - U_unknown_found[i-1]

plt.plot(U_unknown_found)
plt.savefig(f"E-{E}_A-{A}_FORCE-CONSTANT-{FORCE_CONSTANT}_F=Kx_Length-{BAR_LENGTH}_Number_of_elements-{NUMBER_OF_ELEMENTS}_U-{U_SPECIFIED}_Q-{Q_SPECIFIED}.png")
plt.show()
# plt.close()
