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
    policy_cost(config_fname)


def policy_cost(config_fname):
    # check if it is a baseline scenario
    baseline = config_fname.split("_")[0]
    scenario = config_fname.split("_")[1]

    # build and write out scenario policy cost
    supply = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
    price = data_manipulation.get_sensitivity_data([config_fname], "prices_of_all_markets")
    dataframe = pd.merge(supply, price, "left", on=["technology", "GCAM"], suffixes=("_supply", "_demand"))
    marimekko(dataframe)

    if scenario == baseline:
        # this is a baseline scenario and no additional work needs to be done
        pass
    else:
        compare_marimekko()

        # and compare to default


def compare_marimekko():
    pass

def marimekko(df):
    pass


if __name__ == '__main__':
    main("test_default", "2050")
