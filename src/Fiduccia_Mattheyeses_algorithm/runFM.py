from src.Fiduccia_Mattheyeses_algorithm.FM import FM_agorithm
from src import helpers


def runFM(n_iter, solution=None, threshold=0):
    """Runs the Fiduccia-Mattheyesses algorithm"""
    min_cuts_value = None
    vertex_data_dict, max_gain = helpers.preprocess('Graph500.txt')
    fm_instance = FM_agorithm(vertex_data_dict, max_gain)
    if solution is None:
        fm_instance.create_split()
    else:
        fm_instance.set_split(solution)
    fm_instance.calculate_gain()
    fm_instance.fill_buckets()
    fm_instance.calculate_cuts()
    cuts = fm_instance.getCuts()
    track = 0
    for i in range(n_iter):
        last_cuts = cuts
        min_solution, min_cuts_value = fm_instance.fm_pass()
        cuts = min_cuts_value

        fm_instance.total_cuts = min_cuts_value
        fm_instance.reset_gains()
        fm_instance.calculate_gain()
        fm_instance.fill_buckets()
        fm_instance.calculate_cuts()
        if threshold > 0:
            if not (cuts < last_cuts):
                track += 1
                if track > threshold:
                    # print("run FM with", i, "iterations and track was:", track)
                    break
            else:
                track = 0

    final_partition = fm_instance.getPartition()

    return final_partition, min_cuts_value


if __name__ == "__main__":
    """won't run unless the current directory is src"""
    n_iter = 1000
    final_partition, n_cuts = runFM(n_iter)
    print("FM terminated on", n_iter, "passes with resulting solution:\n", final_partition, "\nand", n_cuts, "cuts")
