from meta_heuristic_algorithms.GLS import GLS
from meta_heuristic_algorithms.MLS import MLS
from meta_heuristic_algorithms.ILS import ILS

import os
import time
import pandas as pd


class Experiments:

    def __init__(self, runs):
        self.runs = runs

    def getTimeLimit(self):
        print("calculating time limit based on MLS")
        start = time.perf_counter()
        self.MLS_experiment(runs=1)
        end = time.perf_counter()
        return end - start

    def MLS_experiment(self, runs, time_constr=None):
        if time_constr is not None:
            # Unlimited passes, so we increase pop_size
            # because we have more FM budget
            pop_size = 400
        else:
            # 10.000 passses, so we set pop_size to
            # 120 (best-performing population size)
            pop_size = 120

        MLS_object = MLS(solution_amount=pop_size, string_length=500, max_passes=10000)
        cut_array = []
        for x in range(runs):
            print("MLS now at run:", x)
            cuts, solution = MLS_object.run_MLS(time_constr)
            cut_array.append(cuts)

        return cut_array

    def ILS_experiment(self, time_constr=False, allowed_time=1.0):
        min_cuts = []
        for i in range(self.runs):
            print("ILS now at run:", i)
            ils = ILS()
            min_cuts.append(ils.single_run(time_constr, allowed_time))
        return min_cuts

    def GLS_experiment(self, time_constr=False, allowed_time=1.0):
        # comment this to generate a new initial pop for each run
        if not time_constr:
            gls = GLS(n_iterations=100, fm_passes=100)
        else:
            gls = GLS(n_iterations=999999, fm_passes=10000)

        minimum_cuts = []
        for i in range(self.runs):
            if not time_constr:
                # uncomment this to generate a new initial pop for each run
                # gls = GLS(n_iterations=100, fm_passes=100)
                print("GLS without time constraint now at run:", i)
                min_cut, sol = gls.run()
                minimum_cuts.append(min_cut)
                print("min cut:", min_cut)
            else:
                # uncomment this to generate a new initial pop for each run
                # gls = GLS(n_iterations=999999, fm_passes=10000)
                print("GLS with time constraint now at run:", i)
                min_cut, sol = gls.run(FM_threshold=7, time_constr=time_constr, allowed_time=allowed_time)
                minimum_cuts.append(min_cut)
                print("min cut:", min_cut)
        print(minimum_cuts)
        return minimum_cuts

    def DF_MLS_experiment(self, time_constr=None):
        MLS_object = MLS(None, 500, 10000)
        cut_array = []
        for x in range(self.runs):
            print("DF MLS now at run:", x)
            cuts, solution = MLS_object.run_dfs_mls(1, 2, 20, 100, time_constr)
            cut_array.append(cuts)

        return cut_array

    def getExperiment1Data(self):
        start_mls = time.perf_counter()
        mls_exp1 = self.MLS_experiment(self.runs)
        mls_time = round(time.perf_counter() - start_mls, 2)

        start_ils = time.perf_counter()
        ils_exp1 = self.ILS_experiment()
        ils_time = round(time.perf_counter() - start_ils, 2)

        start_gls = time.perf_counter()
        gls_exp1 = self.GLS_experiment()
        gls_time = round(time.perf_counter() - start_gls, 2)

        start_df_mls = time.perf_counter()
        df_mls_exp1 = self.DF_MLS_experiment()
        df_mls_time = round(time.perf_counter() - start_df_mls, 2)

        times = {"mls": [mls_time], "ils": [ils_time], "gls": [gls_time], "df_mls": [df_mls_time]}
        data = {"mls": mls_exp1, "ils": ils_exp1, "gls": gls_exp1, "df_mls": df_mls_exp1}
        df = pd.DataFrame(data=data,
                          index=[i + 1 for i in range(len(mls_exp1))])
        time_df = pd.DataFrame(data=times)

        df.index.name = "run"

        if not os.path.exists(os.path.dirname(os.getcwd()) + "/results"):
            os.chdir("..")
            os.mkdir("results")

        os.chdir("..")
        df.to_csv("results/exp1_data.csv", index=False)
        time_df.to_csv("results/exp1_times.csv", index=False)
        os.chdir("src")

        return df

    def getExperiment2Data(self, time_limit):
        time_limit = time_limit

        start_mls = time.perf_counter()
        mls_exp2 = self.MLS_experiment(self.runs)
        mls_time = round(time.perf_counter() - start_mls, 2)

        start_ils = time.perf_counter()
        ils_exp2 = self.ILS_experiment(True, time_limit)
        ils_time = round(time.perf_counter() - start_ils, 2)

        start_gls = time.perf_counter()
        gls_exp2 = self.GLS_experiment(True, time_limit)
        gls_time = round(time.perf_counter() - start_gls, 2)

        start_df_mls = time.perf_counter()
        df_mls_exp2 = self.DF_MLS_experiment(time_limit)
        df_mls_time = round(time.perf_counter() - start_df_mls, 2)

        times = {"mls": [mls_time], "ils": [ils_time], "gls": [gls_time], "df_mls": [df_mls_time]}
        data = {"mls": mls_exp2, "ils": ils_exp2, "gls": gls_exp2, "df_mls": df_mls_exp2}
        df = pd.DataFrame(data=data,
                          index=[i + 1 for i in range(len(mls_exp2))])
        time_df = pd.DataFrame(data=times)

        df.index.name = "run"

        if not os.path.exists(os.path.dirname(os.getcwd()) + "/results"):
            os.chdir("..")
            os.mkdir("results")

        os.chdir("..")
        df.to_csv("results/exp2_data.csv", index=False)
        time_df.to_csv("results/exp2_times.csv", index=False)
        os.chdir("src")

        return df


if __name__ == "__main__":
    exps = Experiments(runs=15)
    # exps.ILS_experiment(True, 40)
    exps.GLS_experiment(True, 40)
