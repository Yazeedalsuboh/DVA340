import random
import matplotlib.pyplot as plt


# Extracting Code
cities = []
with open('Assignment 3 berlin52.tsp', 'r') as f:
    lines = f.readlines()
    lines = lines[6:58]
    for line in lines:
        data = line.strip().split()
        city = {'name': float(data[0]), 'x': float(data[1]), 'y': float(data[2])}
        cities.append(city)

# Parameters
n_cities = 52
n_population = 250
mutation_rate = 15

# Main Functions
def parents_genesis(n_population):
    parents = []

    for i in range(n_population):
        path = [1] + random.sample(range(2, n_cities+1), 51)
        parents.append({'path': path, 'fitness': fitness_eval(path)})

    return parents

def fitness_eval(n_offsprings):
    sumDistance = 0
    for i in range(len(n_offsprings)-1):
        cityA = cities[int(n_offsprings[i]-1)]
        cityB = cities[int(n_offsprings[i+1]-1)]
        distance = (int((cityA['x'] - cityB['x'])**2) + int((cityA['y'] - cityB['y'])**2))**0.5
        sumDistance += distance
    return sumDistance

def offsprings_genesis(n_parents):
    x = 0
    z = 0
    new_offsprings = []

    sorted_parents = sorted(n_parents, key=lambda x: x['fitness'])

    for parent in sorted_parents:
        while x == z:    
            x = random.randint(0, (len(n_parents)//3)-1)
            z = random.randint(0, (len(n_parents)//3)-1)

        parent1 = sorted_parents[x]['path']
        parent2 = sorted_parents[z]['path']

        offspring = offspring_crossover(parent1, parent2)
        
        new_offsprings.append({'path': offspring, 'fitness': fitness_eval(offspring)})

 
    return new_offsprings

def offspring_crossover(parent1, parent2):
    cross_point1 = random.randint(1, n_cities-1)
    cross_point2 = random.randint(cross_point1+1, n_cities)

    offspring = [1, 1]
    while len(offspring) != len(set(offspring)):
        offspring = [1]
        listB = parent2[cross_point1:cross_point2]
        
        parentA1 = [x for x in parent1[1:cross_point1] if x not in listB]
        parentA2 = [x for x in parent1[cross_point1:] if x not in listB]

        if cross_point1 % 2 == 0:
            for city in parentA1: offspring.append(city)
            for city in listB: offspring.append(city)
            for city in parentA2: offspring.append(city)
        else:
            for city in parentA2: offspring.append(city)
            for city in listB: offspring.append(city)
            for city in parentA1: offspring.append(city)

        mutate(offspring, n_population)
    
    return offspring

def mutate(n_offspring, end):
    y = random.randint(1,end)
    if y < mutation_rate:
        
        a = random.randint(1, (len(n_offspring)-1))
        b = random.randint(1, (len(n_offspring)-1))
        temp = n_offspring[a]
        n_offspring[a] = n_offspring[b]
        n_offspring[b] = temp
        
        return True
    else:
        return False

def selection(n_parents, n_offsprings):
    new_parents = []

    rand_i_p = random.sample(range(0, n_population), n_population)
    rand_i_o = random.sample(range(0, n_population), n_population)

    for i in range(len(n_parents)):
        parent = n_parents[rand_i_p[i]]
        offspring = n_offsprings[rand_i_o[i]]

        if parent['fitness'] > offspring['fitness']:
            new_parents.append(offspring)
            # mutate(new_parents[i]['path'], n_cities-1)
        else:
            new_parents.append(parent)
            # mutate(new_parents[i]['path'], n_cities-1)

    return new_parents

# Driver Code
parents = parents_genesis(n_population)
offsprings = offsprings_genesis(parents)
selects = selection(parents, offsprings)


best_solutions = []
for i in range(1000):
    nn_offsprings = offsprings_genesis(parents)

    parents = selection(parents, nn_offsprings)
    path_sol = min(parents, key=lambda x: x['fitness'])
    fit_sol = min(ele['fitness'] for ele in parents)
    if i % 50 == 0:
        best_solutions.append(fit_sol)
        print(best_solutions)
        print(fit_sol)
        print(path_sol['path'])
    
    if fit_sol < 9000:
        print(fit_sol)
        print(path_sol)
        print("CONGRATS")
        break

x_values = list(range(0, i+1, 50))
plt.plot(x_values, best_solutions)
plt.xlabel("Population")
plt.ylabel("Fitness")
plt.show()
