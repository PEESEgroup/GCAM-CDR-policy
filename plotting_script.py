import os

import plotting
import data_manipulation
import constants as c
import pandas as pd
import numpy as np
import scipy.stats as stats


def main(config_fname, reference_year):
    """
    Main method for scripts used to plot figures and information for the article
    :return: N/A
    """
    os.makedirs("data/data_analysis/supplementary_tables/" + config_fname.replace("_", "/"), exist_ok=True)
    policy_cost(config_fname, reference_year)


def policy_cost(config_fname, year):
    # check if it is a baseline scenario
    baseline = config_fname.split("_")[1]
    scenario = config_fname.split("_")[0]

    # build and write out scenario policy cost
    supply = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
    supply["Units"] = "Mt $CO_{2}$-eq"
    price = data_manipulation.get_sensitivity_data([config_fname], "prices_of_all_markets")

    # TODO find cost of subsidies and include them in the calculation

    # update the price to $2025USD/t C  from $1975USD/kg C - then to a CO@-eq basis
    price["Units"] = "2025USD/t $CO_{2}$-eq"
    for i in c.GCAMConstants.plotting_x:
        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=197501&year2=202501
        price[str(i)] = price[str(i)] * 6.10 * 1000 / 44 * 12  # $/C * C/CO2 molar ratios
        supply[str(i)] = supply[str(i)] / 12 * 44  # C to CO2

    # merge dataframes and constrain to US regions
    dataframe = pd.merge(supply, price, "left", left_on=["technology", "GCAM"], right_on= ["product", "GCAM"],
                         suffixes=("_supply", "_price"))
    dataframe = dataframe[dataframe["GCAM"].isin(c.GCAMConstants.USA_region)]
    """scenario_df = plotting.plot_marimekko(dataframe, c.GCAMConstants.plotting_x, "_supply", "_price", "product_price",
                            "price of CDR by technology and state", config_fname)

    # and compare costs to default
    if scenario != baseline:
        baseline_df = pd.read_csv("data/data_analysis/supplementary_tables/"+baseline+"/"+baseline+"/price of CDR by technology and state.csv")
        plotting.compare_marimekko(scenario_df, baseline_df, config_fname)"""

    # calculate the total cost and plot
    for i in c.GCAMConstants.plotting_x:
        # "Mt $CO_{2}$-eq"  "2025USD/t $CO_{2}$-eq" factor of a million is added to dollars
        dataframe[str(i)] = dataframe[str(i) + "_supply"] * dataframe[str(i) + "_price"]
    # sum by technology
    dataframe = dataframe.groupby(["product_price"]).sum(min_count=1)
    dataframe = dataframe.reset_index()
    dataframe["Units"] = "Million 2025$USD/yr"
    dataframe['scenario'] = scenario
    dataframe['baseline'] = baseline

    plotting.plot_stacked_bar_product(dataframe, c.GCAMConstants.plotting_x, "product_price", "policy cost by year", config_fname)
    dataframe.to_csv("data/data_analysis/supplementary_tables/" + str(config_fname).replace("_", "/") + "/" +
                     "/policy cost by technology.csv")


if __name__ == '__main__':
    main("test_default", "2050")
