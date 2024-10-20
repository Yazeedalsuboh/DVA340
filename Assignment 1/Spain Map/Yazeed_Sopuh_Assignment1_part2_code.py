import re
import timeit

# Extract the items from the text file
file = open('Assignment 1 Spain map.txt', 'r')
text = file.readlines()

# Building G(n) and H(n) into dictionaries
gOfN = text[5:82]
hOfN = text[85:]

dict_g_n = {}
dict_h_n = {}

for ele in hOfN:
    match = re.search(r'(.*) (\d+)', ele)
    dict_h_n[match.group(1)] = int(match.group(2))

for ele in gOfN:
    match = re.search(r'(.*) (.*) (\d+)', ele)

    if match.group(1) in dict_g_n:
        dict_g_n[match.group(1)].update({match.group(2): int(match.group(3))})
    else:
        dict_g_n[match.group(1)] = {match.group(2): int(match.group(3))}

for city in dict_h_n:
    val_cities = []
    for x in dict_g_n:
        for y in dict_g_n[x]:
            if y == city:
                val_cities.append([x, dict_g_n[x][y]])
    
    for z in val_cities:
        if city in dict_g_n:
            dict_g_n[city].update({z[0]: z[1]})
        else:
            dict_g_n[city] = {z[0]: z[1]}

# Classes
class City:
    def __init__(self, name, h_n):
        self.name = name
        self.connections = []
        self.h_n = h_n

    def add_connection(self, city):
        self.connections.append(city)

class Map:
    def __init__(self, start, goal, dict_h_n, dict_g_n):
        self.cities = {}
        self.start_city = None
        self.goal_city = None
        self.build_map(start, goal, dict_h_n, dict_g_n)

    def build_map(self, start, goal, dict_h_n, dict_g_n):        
        
        for city, h_n in dict_h_n.items():
            
            # Building the city
            city_node = City(city, h_n)
            # 'city_name': city_node_address
            self.cities[city] = city_node

            # If exist as key
            if city in dict_g_n:
                for to_city in dict_g_n[city]:
                    # If city node already exist in the dictionary
                    if to_city in self.cities:
                        city_node.add_connection(self.cities[to_city])
                    else:
                        new_city = City(to_city, dict_h_n[to_city])
                        city_node.add_connection(new_city)
                        self.cities[to_city] = new_city
                        self.build_map(to_city, goal, dict_h_n, dict_g_n)

        self.start_city = self.cities[start]
        self.goal_city = self.cities[goal]

map = Map('Malaga', 'Valladolid', dict_h_n, dict_g_n)

# Algorithms
def a_star():
    f_n_list = []
    main_city = map.start_city
    path = [main_city]
    best_path = []


    while main_city.name != map.goal_city.name:

        if main_city.connections:
            for city in main_city.connections:
                f_n = city.h_n + dict_g_n[main_city.name][city.name]
                f_n_list.append({'city': city, 'f_n': f_n, 'path': path})
    
        main_city = min(f_n_list, key= lambda x: x['f_n'])['city']
        path.append(main_city)
    
    for city in f_n_list:
        if city['city'].name == main_city.name:
            for x in city['path']:
                best_path.append(x.name)
            
            return best_path

def gbfs():
    f_n_list = []
    main_city = map.start_city
    path = [main_city]
    best_path = []

    while main_city.name != map.goal_city.name:

        if main_city.connections:
            for city in main_city.connections:
                f_n = city.h_n
                f_n_list.append({'city': city, 'f_n': f_n, 'path': path})
    
        main_city = min(f_n_list, key= lambda x: x['f_n'])['city']
        path.append(main_city)
    
    for city in f_n_list:
        if city['city'].name == main_city.name:
            for x in city['path']:
                best_path.append(x.name)
            
            return best_path

def calc_distance(path):
    total_distance = 0
    for i in range(len(path)-1):
        total_distance += dict_g_n[path[i]][path[i+1]]
    return total_distance

# Driver Code
path = a_star()
print("A* Search:", path)
print("Distance:", calc_distance(path))
time_taken = timeit.timeit(lambda: a_star(), number=100)
print("Execution Time: ", time_taken)

print("\n")

path = gbfs()
print("Greedy Best First Search:", path)
print("Distance:", calc_distance(path))
time_taken = timeit.timeit(lambda: gbfs(), number=100)
print("Execution Time: ", time_taken)