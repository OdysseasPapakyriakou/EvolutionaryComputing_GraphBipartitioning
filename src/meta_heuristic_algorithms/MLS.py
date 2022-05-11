import random
import math
import copy
import time
from src.Fiduccia_Mattheyeses_algorithm.runFM import *


class MLS:
    """The Multi-start Local Search algorithm"""

    def __init__(self, solution_amount, string_length, max_passes):
        self.solution_amount = solution_amount
        self.string_length = string_length
        self.max_passes = max_passes

    def create_split(self):
        length_vertex_list = self.string_length
        half_length = int(length_vertex_list / 2)
        zero_partition = [0 for i in range(half_length)]
        one_partition = [1 for i in range(half_length)]
        solution = zero_partition + one_partition
        random.shuffle(solution)
        return solution

    def create_solutions(self):
        random_sol_array = []
        for item in range(self.solution_amount):
            sol = self.create_split()
            random_sol_array.append(sol)
        return random_sol_array

    def run_MLS(self, time_constr=None):
        best_sol = math.inf
        best_cuts = math.inf

        # Time constraint code, if time is constrained
        # we set passes to infinity and start tracking
        # elapsed time of the algorithm
        start_time = time.perf_counter()
        # set time constraint to 100.000
        if time_constr is not None:
            self.max_passes = 100000 #

        start_solutions = self.create_solutions()
        passes_per_solution = int(self.max_passes / len(start_solutions))
        print("Each MLS solution gets {} FM passes".format(passes_per_solution))
        for solution in start_solutions:
            current_time = time.perf_counter()

            sol, cuts = runFM(passes_per_solution, solution)
            if cuts <= best_cuts:
                best_cuts = cuts
                best_sol = sol
            if time_constr is not None:
                if (current_time-start_time) > time_constr:
                    return best_cuts, best_sol

        return best_cuts, best_sol

    def run_dfs_mls(self, min_improvement, patience_level, bonus_bound, bonus_multiplier, time_constr=None):
        start_solution = self.create_split()
        pass_count = copy.copy(self.max_passes)
        prev_min_cuts = math.inf
        best_cuts = math.inf
        best_solution = None
        original_patience = patience_level
        current_patience = copy.copy(patience_level)
        solutions_tried = 0

        # Time constraint code, if time is constrained
        # we set passes to infinity and start tracking
        # elapsed time of the algorithm
        start_time = time.perf_counter()
        # We set passes to infinite
        # when working with time constraint
        if time_constr is not None:
            pass_count = math.inf
            self.max_passes = 999999

        for item in range(self.max_passes):
            if pass_count > 0:
                current_time = time.perf_counter()

                start_solution, min_cuts = runFM(1, start_solution)
                pass_count -= 1

                # Improvement is measured by difference
                # between previous minimum cuts and current
                # minimum cuts. Value should decrease..
                improvement = prev_min_cuts - min_cuts
                prev_min_cuts = copy.copy(min_cuts)

                if min_cuts < best_cuts:
                    best_cuts = copy.copy(min_cuts)
                    best_solution = copy.deepcopy(start_solution)
                    # if best_cuts <= bonus_bound:
                    #     print('Best cuts updated to: {} with passes left: {}'.format(best_cuts, pass_count))
                if improvement > min_improvement:
                    if bonus_bound - min_cuts > 0:
                        bonus = (bonus_bound - min_cuts) * bonus_multiplier
                    else:
                        bonus = 0
                    current_patience = original_patience + bonus
                else:
                    current_patience -= 1

                # If there is a time constraint,
                # check if not out of time, if so,
                # return the best cuts, solution
                if time_constr is not None:
                    if (current_time - start_time) > time_constr:
                        return best_cuts, best_solution

                if current_patience <= 0:
                    start_solution = self.create_split()
                    solutions_tried += 1
                    current_patience = original_patience
                    continue

        # print("Deep MLS finished with solutions tried: {}".format(solutions_tried))
        return best_cuts, best_solution


if __name__ == "__main__":
    """won't run unless the current directory is src"""
    mls = MLS(solution_amount=100, string_length=500, max_passes=10000)
    best_cuts, best_sol = mls.run_MLS(time_constr=None)
    print("best cuts:", best_cuts)
    print("and this is the sol:", best_sol)
