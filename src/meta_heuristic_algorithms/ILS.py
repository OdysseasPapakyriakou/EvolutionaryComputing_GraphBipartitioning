import time
import random
from copy import deepcopy
from statistics import mean

from src import helpers
from src.Fiduccia_Mattheyeses_algorithm.FM import FM_agorithm


class ILS:
    """The Iterated Local Search algorithm"""

    def purtubate_solution(self, solution, p_size):
        for key in solution:
            if random.random() < p_size:
                while True:
                    index_to_choose = str(random.randint(1, len(solution)))
                    if solution[key].partition != solution[index_to_choose].partition:
                        # first switch partition of key and other random item to keep equal partition
                        solution[key].partition = 1 - solution[key].partition
                        solution[index_to_choose].partition = 1 - solution[index_to_choose].partition
                        break
        return solution

    def FM_pass(self, fm_instance, iterations):
        # 1000 fm passes
        min_solution = None
        min_cuts_value = None
        for j in range(iterations):
            # reset gains of best solution
            fm_instance.reset_gains()
            # calculate new gain
            fm_instance.calculate_gain()
            fm_instance.fill_buckets()
            fm_instance.calculate_cuts()
            min_solution, min_cuts_value = fm_instance.fm_pass()
        return min_solution, min_cuts_value

    def init_solutions(self):
        solutions = []
        vertex_data_dict, max_gain = helpers.preprocess('Graph500.txt')
        for i in range(5):
            fm_instance = FM_agorithm(vertex_data_dict, max_gain)
            fm_instance.create_split()
            min_solution, min_cuts_value = self.FM_pass(fm_instance, 1000)
            fm_instance.vertex_data_dict = min_solution
            solutions.append((fm_instance, min_cuts_value))
        return solutions

    def ils_pass(self, fm_instance_init, min_cuts_value_init, p_size, allowed_time=1.0, timing=False):
        # run 10 times 1000 fm passes if better then init
        best_cut = min_cuts_value_init
        best_solution = fm_instance_init
        better = 0
        for i in range(10):
            if allowed_time > 0:
                start_ils = time.perf_counter()
                best_solution.vertex_data_dict = self.purtubate_solution(best_solution.vertex_data_dict, p_size)
                dict_new, min_cuts_value_next = self.FM_pass(deepcopy(best_solution), 1000)
                if min_cuts_value_next < best_cut:
                    best_solution.vertex_data_dict = dict_new
                    better += 1
                    # print(min_cuts_value_next)
                    best_cut = min_cuts_value_next
                end_ils = time.perf_counter()
                if timing == True:
                    print("allowed time:", allowed_time)
                    # print(end_ils - start_ils)
                    allowed_time -= (end_ils - start_ils)
                # print(total_time)
        return better, best_cut

    def run_for_best_purmutation(self):
        fm_instances = self.init_solutions()
        # 0.15,0.1,0.09,0.08,0.07,0.05,0.04,0.03,0.02,0.005
        p_sizes = [0.15, 0.1, 0.09, 0.08, 0.07, 0.05, 0.04, 0.03, 0.02, 0.005]
        min_cut_avg = mean([i[1] for i in fm_instances])
        # for every prop
        for p in p_sizes:
            # create fm_instances
            fm_instances_for_p = deepcopy(fm_instances)
            # for every fm_instance
            better_list = []
            min_cut_list = []
            for fm_instance_init, min_cuts_value_init in fm_instances_for_p:
                better, best_cut = self.ils_pass(fm_instance_init, min_cuts_value_init, p)

                better_list.append(better)
                min_cut_list.append(best_cut)
            mean_better_list = mean(better_list)
            mean_min_cut_list = mean(min_cut_list)
            print(min_cut_avg)
            print(mean_better_list)
            print(mean_min_cut_list)

    def single_run(self, timing=False, total_time=1):
        p_size = 0.05
        vertex_data_dict, max_gain = helpers.preprocess('Graph500.txt')
        fm_instance = FM_agorithm(vertex_data_dict, max_gain)
        fm_instance.create_split()
        min_solution, min_cuts_value = self.FM_pass(fm_instance, 1000)
        fm_instance.vertex_data_dict = min_solution
        better, best_cut = self.ils_pass(fm_instance, min_cuts_value, p_size, total_time, timing)
        return best_cut


if __name__ == "__main__":
    """won't run unless the current directory is src"""
    ils = ILS()
    print(ils.single_run())
