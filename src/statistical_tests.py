import os
import pingouin as pg
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def MannWhitneyTest(experiment_data, out_name):
    data = pd.read_csv(experiment_data)
    out_df = pd.DataFrame(columns=["algorithms", "U statistic", "p-value"])
    for i in range(0, len(data.columns)-1):
        for j in range(i+1, len(data.columns)):
            mwu = pg.mwu(data.iloc[:, i], data.iloc[:, j], alternative="two-sided")
            u_statistic = mwu["U-val"][0]
            p_val = mwu["p-val"][0]
            algorithms = data.columns[i] + "_" + data.columns[j]
            test_data = {"algorithms": algorithms, "U statistic": u_statistic, "p-value": p_val}

            out_df = out_df.append(test_data, ignore_index=True)

    if not os.path.exists(os.path.dirname(os.getcwd()) + "/results"):
        os.mkdir("results")

    out_df.to_csv(out_name, index=False)
    return out_df


def boxplots(exp_data, out_name):
    data = pd.read_csv(exp_data)
    n = len(data)
    mls = data["mls"].tolist()
    ils = data["ils"].tolist()
    gls = data["gls"].tolist()
    df_gls = data["df_mls"].tolist()
    new_data = {"algorithm": ["mls"]*n + ["ils"]*n + ["gls"]*n + ["df_mls"]*n,
                "nCuts": mls + ils + gls + df_gls}
    new_df = pd.DataFrame(new_data)

    sns.boxplot(data=new_df, x="algorithm", y="nCuts",
                showmeans=True,
                meanprops={"marker": "o",
                           "markerfacecolor": "white",
                            "markeredgecolor": "black",
                            "markersize": 12})

    sns.stripplot(data=new_df, x="algorithm", y="nCuts",
                  color="black",
                  alpha=0.7)
    plt.suptitle(out_name, y=1, fontsize=15)
    plt.title("minimum cuts for each algorithm\ncomputed over 25 runs",
              y=0.99,
              fontsize=10)

    if not os.path.exists(os.path.dirname(os.getcwd()) + "/results"):
        os.mkdir("results")

    plt.savefig(out_name)
    plt.clf()


def descriptiveStats(experiment_data, out_name, time_data):
    data = pd.read_csv(experiment_data)
    times = pd.read_csv(time_data)
    col = data.loc[:, "mls":"df_mls"]

    algorithms = ["mls", "ils", "gls", "df_ils"]
    means = [round(i, 2) for i in col.mean(axis=0).tolist()]
    medians = [round(i, 2) for i in col.median(axis=0).tolist()]
    stds = [round(i, 2) for i in col.std(axis=0).tolist()]
    time_data = times.iloc[0].tolist()

    descriptives = {"algorithm": algorithms, "means": means, "medians": medians, "stds": stds, "cpu_time": time_data}
    out_df = pd.DataFrame(data=descriptives)

    if not os.path.exists(os.path.dirname(os.getcwd()) + "/results"):
        os.mkdir("results")

    out_df.to_csv(out_name, index=False)


if __name__ == "__main__":
    # MannWhitneyTest("exp1_data.csv")
    descriptiveStats("exp2_data.csv", "exp2_descriptives.csv", time_data="exp2_times.csv")
    boxplots("exp2_data.csv", "exp2_boxplots")

