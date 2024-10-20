import random
import matplotlib.pyplot as plt

# Extracting Code
n_cities = []
with open('Assignment 3 berlin52.tsp', 'r') as f:
    lines = f.readlines()
    lines = lines[6:58]
    for line in lines:
        data = line.strip().split()
        city = {'name': float(data[0]), 'x': float(data[1]), 'y': float(data[2])}
        n_cities.append(city)

cities = []
for cityA in n_cities:
    row = []
    for cityB in n_cities:
        row.append((int((cityA['x'] - cityB['x'])**2) + int((cityA['y'] - cityB['y'])**2))**0.5)
    cities.append(row)


# Parameters
N = 3 # Number of ants
a = 2 # Alpha
b = 4 # Beta
p = 0.7 # Evaporation Coefficient


# Algorithm
def visibility_genesis():
    n_visibility_matrix = []

    for row in cities:
        visibility_row = []
        for d in row:
            if d != 0:
                visibility = round(1/d, 4)
                visibility_row.append(visibility)
            else:
                visibility_row.append(0)
        n_visibility_matrix.append(visibility_row)

    return n_visibility_matrix

def set_visibility_zero(n_visibility_matrix, next_city_index = 0):
   
    for i in range(len(n_visibility_matrix)):
        for j in range(len(n_visibility_matrix)):
            if j == next_city_index:
                n_visibility_matrix[i][j] = 0


    return n_visibility_matrix

def t_n_genesis(n_visibility_matrix, phermones_matrix, next_city_index = 0):
    sum_t_n = 0
    all_t_n = []

    for i in range(len(cities)):
        t_n = (phermones_matrix[next_city_index][i]**a) * (n_visibility_matrix[next_city_index][i]**b)
        sum_t_n += t_n
        all_t_n.append(t_n)
    
    return sum_t_n, all_t_n

def probability_genesis(n_sum_t_n, n_all_t_n):

    probabilities = []
    if n_sum_t_n != 0:
        for t_n in n_all_t_n:
            probabilities.append(round(t_n/n_sum_t_n, 6))
    else:
        for t_n in n_all_t_n:
                probabilities.append(0)

    cumulative_probabilities = [probabilities[0]]
    for i in range(1, len(probabilities)):
        cumulative_probabilities.append(cumulative_probabilities[-1] + probabilities[i])

    return probabilities, cumulative_probabilities

def next_city_genesis(n_cumulative_probabilities):
    r = round(random.uniform(0, 1), 4)
    next_city = 0
    next_city_index = 0
    if (n_cumulative_probabilities[0] > r):
            next_city = n_cumulative_probabilities[0]
            next_city_index = 0
    else:
        for i in range(len(n_cumulative_probabilities)-1):
            cityA = n_cumulative_probabilities[i]
            cityB = n_cumulative_probabilities[i+1]

            if (cityA < r) and (cityB > r):
                next_city = cityB
                next_city_index = i+1
    
    return next_city, next_city_index

def phermones_update(path, phermones_matrix):
    phermone = 1/calc_distance(path)

    for i in range(len(path)-1):
        if phermones_matrix[path[i]][path[i+1]] == p:
            phermones_matrix[path[i]][path[i+1]] = round(phermone + p, 4)
        else:
            phermones_matrix[path[i]][path[i+1]] = round(phermones_matrix[path[i]][path[i+1]] + phermone, 4)

    return phermones_matrix

def calc_distance(path):
    total_distance = 0
    for i in range(len(path)-1):
        total_distance += cities[path[i]][path[i+1]]
    return total_distance

def run_ant(phermones_matrix):
    
    visibility_matrix = visibility_genesis()

    path = [0]
    next_city_index = 0

    for i in range(len(cities)-1):
        visibility_matrix = set_visibility_zero(visibility_matrix, next_city_index)
        
        sum_t_n, all_t_n = t_n_genesis(visibility_matrix, phermones_matrix, next_city_index)

        probabilities, cumulative_probabilities = probability_genesis(sum_t_n, all_t_n)

        next_city, next_city_index = next_city_genesis(cumulative_probabilities)

        path.append(next_city_index)
        
    path.append(0)
    phermones_matrix = phermones_update(path, phermones_matrix)
    return calc_distance(path), path


# Driver Code
phermones_matrix = []
best_solutions = []

best_solution = 60000
x_values = []
for i in cities:
    row = []
    for j in cities:
        row.append(1)
    phermones_matrix.append(row)

for i in range(25000):
    new_distance, new_path = run_ant(phermones_matrix)

    if best_solution > new_distance:
        best_solution = new_distance
        x_values.append(i)
        best_solutions.append(best_solution)
        if best_solution < 9000:
            print(new_path
                  )
            print(best_solution)
            break

plt.plot(x_values, best_solutions)
plt.xlabel("Ants")
plt.ylabel("Fitness")
plt.show()
