#=================================================================================================================================
import numpy as np
import matplotlib.pyplot as plt
#=================================================================================================================================
# You can adjust these problem solving constants according to your needs to find the optimal solution.
max_iterations = 1000 # Number of attempts to find a better answer
n_ant          = 8    # Number of ants
alpha          = 1.0  # The ratio of inclination to the more pheromone
beta           = 0.2  # The ratio of inclination to the shorter path
rho            = 0.1  # The percentage of pheromone evaporation after each iteration
Q              = 1    # Pheromone quota of each ant in each iteration
#=================================================================================================================================
# Create an N*2 numpy array to store the coordinates of cities
# You can specify the values of this array as desired
cities = np.random.choice(np.arange(-100, 100), replace=False, size=8*2).reshape(8, 2)
n_cities = len(cities) # Number of cities
#=================================================================================================================================
class Ant:
    # Information of ants at each iteration
    path = []
    cost = 0

ants = [Ant for it in range(n_ant)]
#=================================================================================================================================
# The final answer to the problem
best_path = []
best_path_cost = np.inf
#=================================================================================================================================
# Create a numpy array representation as an adjacency matrix to hold the distance between cities
distance_matrix = np.ones(shape=(n_cities, n_cities))

# Fill the distance matrix with the distances of the cities
for row, value in enumerate(distance_matrix):
    for column, distance in enumerate(value):
        distance_matrix[row][column] = np.sqrt((cities[row][0] - cities[column][0])**2 + (cities[row][0] - cities[column][0])**2)
#=================================================================================================================================
# Create a numpy array representation as an adjacency matrix to hold the pheromone value between cities
# To begin with, the value of this pheromone matrix is the same for all cities
pheromone_matrix = np.ones(shape=(n_cities, n_cities))
#=================================================================================================================================
def path_selection(current_city):
    # The first step of the main loop: finding a path with a random start
    unseens_city = [it for it in range(n_cities)]
    path         = [current_city]

    for state in range(n_cities - 1):
        unseens_city.remove(current_city)
        option = np.ones_like(unseens_city, dtype=np.float64)
        for index, value in enumerate(unseens_city):
            option[index] = float((pheromone_matrix[current_city][value]**alpha) * (distance_matrix[current_city][value]**beta))
        p = option / np.sum(option) # Normalization of weight score of candidate paths
        current_city = np.random.choice(unseens_city, 1, p=p)[0] # A weighted choice from the candidate paths
        path.append(current_city)

    else:
        path.append(path[0])

    return path
#=================================================================================================================================
def path_cost(path):
    # The second step of the main loop: calculating the length of a traveled path
    cost = 0
    for index, value in enumerate(path[:-1]):
        cost += distance_matrix[value][path[index+1]]
    return float(cost)
#=================================================================================================================================
def update_pheromone():
    # The third stage of the main loop: increasing the amount of pheromone of the traveled routes
    global pheromone_matrix
    for ant in ants:
        for index, value in enumerate(ant.path[:-1]):
            pheromone_matrix[value][ant.path[index+1]] += (Q / ant.cost)
            pheromone_matrix[ant.path[index+1]][value] += (Q / ant.cost)
    pheromone_matrix *= float(1 - rho)
#=================================================================================================================================
def visualiton(it, ant):
    # Update and display the best path found and its length in the output.
    global best_path
    global best_path_cost
    if ant.cost < best_path_cost:
        best_path = ant.path
        best_path_cost = ant.cost
        print(it)
        print(best_path)
        print(best_path_cost)
        plt.clf()
        plt.xticks([])
        plt.yticks([])
        plt.xlim(-100, +100)
        plt.ylim(-100, +100)
        plt.grid(True, color='black', zorder=-1)
        plt.title(label = f"BEST PATH COST: {best_path_cost:f}", pad = 20)
        plt.plot([cities[it][0] for it in best_path], [cities[it][1] for it in best_path], marker="o", color="k", mfc="r")

        plt.pause(1) #You can modify this value to control changing speed.
#=================================================================================================================================
for it in range(max_iterations):
    for ant in ants:
        initial_city = np.random.randint(0, n_cities)
        ant.path = path_selection(initial_city)
        ant.cost = path_cost(ant.path)
        visualiton(it, ant)
    update_pheromone()

plt.show()
#=================================================================================================================================