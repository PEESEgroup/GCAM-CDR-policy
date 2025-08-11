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
    baseline = config_fname.split("_")[0]
    scenario = config_fname.split("_")[1]


if __name__ == '__main__':
    main("default_test", "2050")
