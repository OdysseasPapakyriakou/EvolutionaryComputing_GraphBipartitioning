import time
import operator

from src.Fiduccia_Mattheyeses_algorithm.runFM import *
from src.Fiduccia_Mattheyeses_algorithm.FM import *


class GLS:
    """The Genetic Local Search algorithm"""

    vertex_data_dict, max_gain = helpers.preprocess("Graph500.txt")
    length = len(vertex_data_dict)
    pop_size = 50

    def __init__(self, n_iterations, fm_passes):
        self.n_iterations = n_iterations
        self.fm_passes = fm_passes
        self.init_pop = self.InitPopulation()

    def InitPopulation(self) -> list[list]:
        print("generating initial population for GLS")
        half_length = int(len(self.vertex_data_dict)/2)
        optimized_population = []
        while len(optimized_population) < self.pop_size:
            solution = [0] * half_length + [1] * half_length
            random.shuffle(solution)
            # avoids duplicate solutions
            if solution not in optimized_population:
                opt_sol, cuts = runFM(n_iter=100, solution=solution)
                optimized_population.append(opt_sol)

        return optimized_population

    def selectParents(self, population: list[list]) -> "parent1: list, parent2: list":
        parents = random.sample(range(0, len(population)), k=2)
        return population[parents[0]], population[parents[1]]

    def isValidSolution(self, solution: list) -> bool:
        return sum(solution) == (self.length/2)

    def hammingDistance(self, x: list, y: list) -> tuple[int, set[int]]:
        assert len(x) == len(y), "iterables x and y must have equal length"
        similar_indices = set()
        similarity = 0
        for index, (xi, yi), in enumerate(zip(x, y)):
            if xi == yi:
                similarity += 1
                similar_indices.add(index)
        return self.length - similarity, similar_indices

    def invertBits(self, parent1: list, parent2: list) -> tuple[list, list]:
        if random.randint(0, 1) == 0:
            return [1 if i == 0 else 0 for i in parent1], parent2
        else:
            return parent1, [1 if i == 0 else 0 for i in parent2]

    def generateChild(self, parent1: list, parent2: list) -> list:
        d, similar_indices = self.hammingDistance(parent1, parent2)
        if d > self.length/2:
            parent1, parent2 = self.invertBits(parent1, parent2)

        child = [None] * self.length
        for i in similar_indices:
            # assert parent1[i] == parent2[i], "oops, sth went wrong!"
            child[i] = parent1[i]

        # I want the indices that are in all_indices but not in sim_indices
        all_indices = set(i for i in range(self.length))
        dif_indices = list(all_indices - similar_indices)
        # assert len(dif_indices) % 2 == 0, "initial solution is not balanced"
        half = int(len(dif_indices)/2)
        rem_parts = [0] * half + [1] * half
        # assert len(rem_parts) == len(dif_indices), "length of remaining parts and different indices is not equal"
        random.shuffle(dif_indices)
        for i, index in enumerate(dif_indices):
            child[index] = rem_parts[i]

        return child

    def evaluateFitness(self, solution: list) -> int:
        for i, key in enumerate(self.vertex_data_dict):
            self.vertex_data_dict[key].partition = solution[i]

        nCuts = 0
        checked_ids = []
        for key in self.vertex_data_dict:
            v = self.vertex_data_dict[key]
            checked_ids.append(v.number)
            for n in v.neighbors:
                n_vertex = self.vertex_data_dict[n]
                if v.partition != n_vertex.partition and n not in checked_ids:
                    nCuts += 1
        return nCuts

    def rankAllFitness(self, population: list[list]) -> list[tuple[int, list]]:
        fitnesses = []
        for sol in population:
            fitnesses.append(self.evaluateFitness(sol))
        zipped = zip(fitnesses, population)
        # larger first
        zipped = sorted(zipped, key=operator.itemgetter(0), reverse=True)
        return zipped

    def replace(self, optimize_child: list, child_cuts: int, zipped: list[tuple[int, list]]):
        fitnesses, pop = map(list, zip(*zipped))
        if optimize_child not in pop and child_cuts < zipped[0][0]:
            zipped[0] = (child_cuts, optimize_child)
        # larger first
        zipped = sorted(zipped, key=operator.itemgetter(0), reverse=True)
        fitnesses, pop = map(list, zip(*zipped))

        return fitnesses, pop, zipped

    def run(self, FM_threshold: int=0, time_constr=False, allowed_time=1.0):
        new_fitnesses = None
        zipped = self.rankAllFitness(self.init_pop)
        pop = self.init_pop

        for i in range(self.n_iterations):
            if allowed_time > 0.0:
                start_GLS = time.perf_counter()
                # if i % 50 == 0:
                    # print("gls now at", i, "iterations")
                parent1, parent2 = self.selectParents(pop)
                child = self.generateChild(parent1, parent2)
                optimized_child, cuts = runFM(n_iter=self.fm_passes, threshold=FM_threshold, solution=child)
                new_fitnesses, pop, zipped = self.replace(optimized_child, cuts, zipped)

                # print("optimized child:", cuts)
                end_GLS = time.perf_counter()

                if time_constr:
                    allowed_time -= (end_GLS - start_GLS)
        # smaller (best) first
        result = sorted(zip(new_fitnesses, pop), key=operator.itemgetter(0))[0]
        return result[0], result[1]


if __name__ == "__main__":
    """won't run unless the current directory is src"""
    GLS = GLS(n_iterations=100, fm_passes=100)
    GLS.run()




