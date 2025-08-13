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
    policy_cost(config_fname, reference_year)


def policy_cost(config_fname, year):
    # check if it is a baseline scenario
    baseline = config_fname.split("_")[0]
    scenario = config_fname.split("_")[1]

    # build and write out scenario policy cost
    supply = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
    price = data_manipulation.get_sensitivity_data([config_fname], "prices_of_all_markets")

    # update the price to $2025USD/t C  from $1975USD/kg C
    price["Units"] = "2025$/t C"
    for i in c.GCAMConstants.plotting_x:
        # https://data.bls.gov/cgi-bin/cpicalc.pl?cost1=1.00&year1=197501&year2=202501
        price[str(i)] = price[str(i)] * 6.10 * 1000

    dataframe = pd.merge(supply, price, "left", left_on=["technology", "GCAM"], right_on= ["product", "GCAM"],
                         suffixes=("_supply", "_price"))

    # calculate the total cost
    for i in c.GCAMConstants.plotting_x:
        dataframe[str(i) + "_total-cost"] = dataframe[str(i) + "_supply"] * dataframe[str(i) + "_price"]

    plotting.plot_marimekko(dataframe, year, "total policy cost by technology and state")
    plotting.plot_stacked_bar_product(dataframe, c.GCAMConstants.plotting_x, "technology", "policy cost by year", config_fname)

    if scenario == baseline:
        # this is a baseline scenario and no additional work needs to be done
        pass
    else:
        # and compare to default
        plotting.compare_marimekko()


if __name__ == '__main__':
    main("test_default", "2050")
