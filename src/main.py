from experiments import *
from statistical_tests import *


def main():
    """run any code here"""
    exps = Experiments(runs=25)
    exps.getExperiment1Data()
    time_limit = exps.getTimeLimit()
    exps.getExperiment2Data(time_limit=time_limit)

    os.chdir("../results")
    descriptiveStats(experiment_data="exp1_data.csv", time_data="exp1_times.csv", out_name="exp1_descriptives.csv")
    descriptiveStats(experiment_data="exp2_data.csv", time_data="exp2_times.csv", out_name="exp2_descriptives.csv")

    boxplots("exp1_data.csv", "exp1_boxplots")
    boxplots("exp2_data.csv", "exp2_boxplots")

    MannWhitneyTest("exp1_data.csv", "exp1_stat_results.csv")
    MannWhitneyTest("exp2_data.csv", "exp2_stat_results.csv")

    os.chdir("../src")


main()
# os.chdir("../results")
# MannWhitneyTest("exp1_data.csv", "exp1_stat_results.csv")
# MannWhitneyTest("exp2_data.csv", "exp2_stat_results.csv")
# os.chdir("../src")
