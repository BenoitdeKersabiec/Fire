import pandas as pd
import numpy as np
from sacred import Experiment
import matplotlib.pyplot as plt
from plot import plot_data
import multiprocessing
import tqdm

ex = Experiment("FIRE")


@ex.config
def config():
    mode = "simulate"

    start_date = "01/07/2022"
    # Investment details
    monthly_investment = 800
    investment_annual_growth_rate = 0.1
    annual_return = 0.08
    annual_standard_deviation = 0.15

    retirement_date = "01/01/2060"
    retirement_percentage = 0.04

    end_date = "01/01/2080"

    save_resutls_to_csv = True


@ex.capture
def simulate(
        start_date,

        monthly_investment,
        investment_annual_growth_rate,
        annual_return,
        annual_standard_deviation,

        retirement_date,
        retirement_percentage,

        end_date,

        save_resutls_to_csv,
        plot=True
):
    data = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq="MS"))

    # How much you invest every month
    monthly_investment_increase = (1 + investment_annual_growth_rate) ** (1 / 12)
    data["Investment growth rate"] = pd.Series(monthly_investment_increase, index=data.index).shift(1).fillna(1)
    data["Investment"] = monthly_investment * data["Investment growth rate"].cumprod()
    data.loc[data.index >= retirement_date, "Investment"] = 0

    data["Total investment"] = data["Investment"].cumsum()

    data["Annual earning rate"] = pd.Series(
        np.random.normal(annual_return, annual_standard_deviation, len(data)),
        index=data.index
    )
    data.loc[data.index >= retirement_date, "Annual earning rate"] -= retirement_percentage

    data["Net worth"] = 0
    for i in range(1, len(data)):
        date = data.index[i]
        data.loc[date, "Net worth"] = \
            data.iloc[i - 1]["Net worth"] * ((1 + data.iloc[i]["Annual earning rate"]) ** (1 / 12)) \
            + data.iloc[i]["Investment"]  # Previous net-worth * earning rate  + Monthly investment

    data["Wage rate"] = 0
    data.loc[data.index >= retirement_date, "Wage rate"] = retirement_percentage
    data["Wage"] = data["Net worth"] * data["Wage rate"]

    if save_resutls_to_csv:
        data.to_csv("output.csv")
        print("Results are saved to 'output.csv'")

    if plot:
        plot_data(data[["Net worth", "Wage"]])
        plt.show()

    return data.loc[retirement_date, "Wage"]


def aux(retirement):
    return simulate(
        retirement_date=retirement,
        plot=False,
        end_date=retirement + pd.to_timedelta("1 days"),
        save_resutls_to_csv=False
    )


@ex.capture
def find_best_retirement_date(start_date, end_date, save_resutls_to_csv):
    print("---------------------- Running evaluation to compute the first retirement wage ---------------------")
    data = pd.DataFrame(index=pd.date_range(start=start_date, end=end_date, freq="MS"))
    print(f"Starting computation for the {len(data)} dates")
    with multiprocessing.Pool() as date_pool:
        results = list(tqdm.tqdm(date_pool.imap_unordered(aux, data.index), total=len(data)))

    # Use the fact that the results are strictly increasing
    results.sort()
    data["First retirement wage"] = results

    if save_resutls_to_csv:
        data.to_csv("output.csv")
        print("Results are saved to 'output.csv'")

    data.plot(logy=True, xlabel="Retirement date", ylabel="???")
    plt.show()


@ex.automain
def main(mode):
    assert mode in ["simulate", "eval"], "Invalid mode"

    if mode == "simulate":
        print("---------------------------------------- Starting simulation ---------------------------------------")
        simulate()

    if mode == "eval":
        find_best_retirement_date()
