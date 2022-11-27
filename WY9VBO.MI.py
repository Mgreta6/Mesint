import numpy as np


class GenExercise:
    # ez a class generalja random szamokkal a koordinatakat, es abbol a matrixot a feladathoz

    def __init__(self, seed: int, num_of_cities: int, num_of_vehicles: int, num_of_iterations: int):
        self.seed = seed
        self.num_of_cities = num_of_cities
        self.num_of_vehicles = num_of_vehicles
        self.num_of_iterations = num_of_iterations

    # ez a method generalja a koordinataka
    def generate_coordinates(self):
        np.random.seed(self.seed)
        return np.random.randint(1000, size=(self.num_of_cities, 2))

    # ez rendezi a koordinatakat matrixba es szamolja a tavolsagokat Manhattan tavolsag szerint
    def coordinates_to_adjacency_matrix(self):
        self.data = self.generate_coordinates()
        a = np.zeros((len(self.data), len(self.data)))
        for i in range(len(a)):
            for j in range(len(a)):
                if not i == j:
                    a[i][j] = np.linalg.norm(sum(abs(val1 - val2) for val1, val2 in zip(self.data[i], self.data[j])))
        return a


class Chromosome():
    # ebben a classben fut az algoritmus, ami az inputalt matrix alapjan ertekeli a varosok kozti tavolsagokat,
    # es a lehetseges megoldasok alapjan utvonalakat kepez a jarmuveknek

    # Random generated Chromosome
    #  m - az utazo ugynokok vagy a jarmuvek szama
    #  n - a varosok szama
    #  adj - az algoritmusba betaplalt matrix, erre fentebb van a GenExercise class, ahol random szamokat generalva
    #  aztan matrixba rendezve kapunk egy output matrixot amit itt használ az algoritmus
    def __init__(self, number_of_cities, number_of_traveling_salesman, adj):
        self.n = number_of_cities
        self.m = number_of_traveling_salesman
        self.adj = adj
        c = np.array(range(1, number_of_cities))
        np.random.shuffle(c)
        self.solution = np.array_split(c, self.m)
        for i in range(len(self.solution)):
            self.solution[i] = np.insert(self.solution[i], 0, 0)
            self.solution[i] = np.append(self.solution[i], 0)
        self.fitness()

    # Evaluate the Chromosome - Fitness function
    #  2 szempont szerint:
    #   - teljes koltseg
    #   - a legrosszabb (leghosszabb) ugynok/jarmu koltsege
    def fitness(self):
        self.cost = 0
        longest_salesman_fitness = []
        longest_salesman_length = 0
        for i in range(self.m):
            salesman = self.solution[i]
            salesman_fitness = 0
            for j in range(len(salesman) - 1):
                salesman_fitness = salesman_fitness + self.adj[salesman[j]][salesman[j + 1]]
                # print(salesman_fitness)
                # print(j)
                # print(self.adj[salesman[j]][salesman[j+1]])
            self.cost = self.cost + salesman_fitness
            if len(salesman) > longest_salesman_length or (
                    len(salesman) == longest_salesman_length and salesman_fitness > self.minmax):
                longest_salesman_length = len(salesman)
                self.minmax = salesman_fitness
        self.score = self.cost + self.minmax


class Population():
    # ebben a classban tortenik az adott feladat parametereinek inputalasa, majd azok futtatasa a Chromosome class-ben
    # ahol a tenyleges algoritmus fut

    def __init__(self, population_size, num_of_cities, num_of_iterations, adj):
        self.population = []
        self.num_of_cities = num_of_cities
        self.population_size = population_size
        self.num_of_iterations = num_of_iterations
        self.adj = adj
        for i in range(population_size):
            self.population.append(
                Chromosome(number_of_cities=self.num_of_cities, number_of_traveling_salesman=self.population_size,
                           adj=GenExercise(1000,
                                           self.num_of_cities,
                                           self.population_size,
                                           self.num_of_iterations).coordinates_to_adjacency_matrix()))


    # Print teljes koltseg es a minmax koltsege a legjobb chromosome-nak
    # ez nincs meghivva sehol kesobb, ez csak egy ellenorzo metodus szamomra
    def get_best_result(self):
        best_chromosome = self.population[0]
        for i in range(1, self.population_size):
            if self.population[i].score < best_chromosome.score:
                best_chromosome = self.population[i]
        print("Overall cost: ", best_chromosome.cost)
        print("Minmax cost: ", best_chromosome.minmax)


class RunResults:
    # ez a class az algoritmus megoldasaibol a legjobb megoldast valasztja ki

    def __init__(self, num_of_vehicles, num_of_cities, num_of_iterations):
        self.population_size = num_of_vehicles
        self.num_of_cities = num_of_cities
        self.num_of_iterations = num_of_iterations
        self.pop = Population(population_size=self.population_size,
                              num_of_cities=self.num_of_cities,
                              num_of_iterations=self.num_of_iterations,
                              adj=GenExercise(1000, self.num_of_cities, self.population_size,
                                              self.num_of_iterations).coordinates_to_adjacency_matrix())

    # Iteraljon vegig a populacion es keresse meg a legjobb megoldast
    def iter_pop(self):
        self.best_chromosome = self.pop.population[0]
        for i in range(1, self.pop.population_size):
            if self.pop.population[i].score < self.best_chromosome.score:
                best_chromosome = self.pop.population[i]

    # Print legjobb megoldast
    def best_sol(self):
        for i in range(self.best_chromosome.m):
            print(i + 1, ":  ", self.best_chromosome.solution[i][0] + 1, end="", sep="")
            for j in range(1, len(self.best_chromosome.solution[i])):
                print("-", self.best_chromosome.solution[i][j] + 1, end="", sep="")
            print(" --- #", len(self.best_chromosome.solution[i]))
        print()

    # Print koltseg
    def print_cost(self):
        print("Total distance of all paths: \t\t", self.best_chromosome.cost)
        print("Minimum distance by the vehicles: \t", self.best_chromosome.minmax)


########################################################################################################################


run = RunResults(num_of_vehicles=4, num_of_cities=10, num_of_iterations=1000)
run.iter_pop()
run.best_sol()
run.print_cost()