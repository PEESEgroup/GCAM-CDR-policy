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
    if scenario == baseline:
        # TODO build and write out baseline scenario
        supply = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
        price = data_manipulation.get_sensitivity_data([config_fname], "CDR_by_tech")
    else:
        # TODO build and write out scenario policy cost, and compare to default
        pass


def marimekko(df):
    pass

if __name__ == '__main__':
    main("default_test", "2050")
